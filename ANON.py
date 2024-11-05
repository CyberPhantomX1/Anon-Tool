import os
import time
import requests
import platform
from stem import Signal
from stem.control import Controller
import logging
import argparse
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(filename='tor_tool.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    """Display a banner at the start of the tool."""
    banner = """
    ===============================
            ANON TOOL v1.0
        Your Privacy Companion
    ===============================
    """
    print(banner)

def log_event(event, level="info"):
    if level == "info":
        logging.info(event)
    elif level == "error":
        logging.error(event)

# Tor password from environment variable
TOR_PASSWORD = os.getenv('TOR_PASSWORD', '')

def renew_tor_ip():
    """Renew the Tor IP address."""
    try:
        log_event("Renewing Tor IP...")
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)

            # Wait for Tor circuit to become available dynamically
            while not controller.is_newnym_available():
                time.sleep(0.5)  # Polling every 0.5 seconds

            log_event("Tor IP renewed successfully.")
    except Exception as e:
        log_event(f"Failed to renew Tor IP: {e}", level="error")

def get_tor_exit_ip():
    """Retrieve the current Tor exit IP using an external service."""
    try:
        proxies = {
            "http": "socks5://127.0.0.1:9050",
            "https": "socks5://127.0.0.1:9050"
        }
        response = requests.get('https://ipinfo.io/ip', proxies=proxies, timeout=5)
        exit_ip = response.text.strip()
        log_event(f"Current Tor Exit IP: {exit_ip}")
        print(f"Current Tor Exit IP: {exit_ip}")
        return exit_ip
    except Exception as e:
        log_event(f"Failed to retrieve Tor Exit IP: {e}", level="error")
        return None

def request_with_retries(url, headers, max_retries=2):
    """Request with retries and enforce HTTPS, using dynamic timeouts."""
    if not url.startswith("https"):
        log_event(f"Attempted to access insecure HTTP URL: {url}", level="error")
        return None
    
    proxies = {
        "http": "socks5://127.0.0.1:9050",
        "https": "socks5://127.0.0.1:9050"
    }

    timeout = 5  # Initial timeout

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            log_event(f"Request to {url} successful.")
            return response
        except requests.RequestException as e:
            log_event(f"Request failed (Attempt {attempt+1}/{max_retries}): {e}", level="error")
            timeout += 2  # Increment timeout for next retry
            time.sleep(1)  # Reduced retry delay
    log_event(f"Max retries reached for {url}, giving up.", level="error")
    return None

def automatic_mode(interval):
    """Automatic mode for renewing IP every interval seconds."""
    while True:
        renew_tor_ip()
        get_tor_exit_ip()  # Check the current Tor exit IP
        time.sleep(interval)

def manual_mode():
    """Manual mode for renewing IP on user input."""
    while True:
        user_input = input("Do you want to renew your IP? (y/n): ")
        if user_input.lower() == 'y':
            renew_tor_ip()
            get_tor_exit_ip()  # Check the current Tor exit IP
        elif user_input.lower() == 'n':
            break
        else:
            print("Invalid input, please type 'y' or 'n'.")

def clear_logs():
    """Clear logs to remove traces of the tool usage."""
    try:
        with open('tor_tool.log', 'w'):
            pass  # Truncate the log file
        log_event("Logs cleared successfully.")
    except Exception as e:
        log_event(f"Failed to clear logs: {e}", level="error")

def kill_switch():
    """Kill switch functionality to block traffic if Tor disconnects."""
    try:
        log_event("Activating Kill Switch...")
        if platform.system() == "Linux":
            os.system("sudo iptables -I OUTPUT -m conntrack --ctstate NEW -j DROP")
            log_event("Kill switch activated (Linux).")
        elif platform.system() == "Windows":
            os.system("netsh interface set interface 'Wi-Fi' admin=disable")
            log_event("Kill switch activated (Windows).")
    except Exception as e:
        log_event(f"Failed to activate Kill Switch: {e}", level="error")

def disable_kill_switch():
    """Disable the kill switch after safely shutting down Tor."""
    try:
        log_event("Disabling Kill Switch...")
        if platform.system() == "Linux":
            os.system("sudo iptables -D OUTPUT -m conntrack --ctstate NEW -j DROP")
            log_event("Kill switch disabled (Linux).")
        elif platform.system() == "Windows":
            os.system("netsh interface set interface 'Wi-Fi' admin=enable")
            log_event("Kill switch disabled (Windows).")
    except Exception as e:
        log_event(f"Failed to disable Kill Switch: {e}", level="error")

def auto_detect_tor_connectivity():
    """Auto-detect Tor connectivity issues and retry connection if failed."""
    try:
        log_event("Checking Tor connectivity...")
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            if not controller.is_newnym_available():
                log_event("Tor connection is unstable or down. Attempting reconnection...", level="error")
                renew_tor_ip()
                print("Tor connection restored.")
            else:
                log_event("Tor is connected and stable.")
    except Exception as e:
        log_event(f"Failed to check Tor connectivity: {e}", level="error")

# Command-line interface using argparse
def main():
    display_banner()  # Display banner on start
    parser = argparse.ArgumentParser(description="Tor IP Change Tool with Enhanced Security Features and Latency Optimizations")
    parser.add_argument('-m', '--mode', choices=['manual', 'automatic'], required=True,
                        help="Choose the mode of operation")
    parser.add_argument('-i', '--interval', type=int, default=300,
                        help="Interval between automatic IP changes (seconds)")
    parser.add_argument('--clear-logs', action='store_true',
                        help="Clear logs after session ends")
    parser.add_argument('--activate-kill-switch', action='store_true',
                        help="Activate kill switch for added protection")
    parser.add_argument('--disable-kill-switch', action='store_true',
                        help="Disable kill switch when done")
    parser.add_argument('--check-tor-connection', action='store_true',
                        help="Check and reconnect if Tor is unstable")

    args = parser.parse_args()

    if args.activate_kill_switch:
        kill_switch()

    if args.check_tor_connection:
        auto_detect_tor_connectivity()

    if args.mode == 'automatic':
        automatic_mode(args.interval)
    elif args.mode == 'manual':
        manual_mode()

    if args.clear_logs:
        clear_logs()

    if args.disable_kill_switch:
        disable_kill_switch()

if __name__ == "__main__":
    main()
