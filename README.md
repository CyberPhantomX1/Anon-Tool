# Anon-Tool
Anon is a powerful anonymity tool designed to enhance privacy and security while browsing the internet and accessing the dark web. It integrates seamlessly with the Tor network and enables users to change their IP addresses dynamically, enforcing HTTPS requests, blocking insecure connections, and preventing IP leakage with a kill switch feature. 

##Why We Made This Tool?
Anon was created to provide a more robust and customizable solution for anonymity than other tools
available in the market. Unlike basic anonymity browsers, Anon offers features like Tor IP renewal,
HTTPS enforcement, a kill switch, and the ability to clear logs, giving users greater control over their
privacy.
Compared to other tools, Anon offers:
1. Dynamic IP change through the Tor network.
2. HTTPS-only enforced browsing for better security.
3. A kill switch that blocks internet traffic if the Tor network fails.
4. Customizable manual or automatic modes for IP renewal.

#Detailed Setup
To get started with Anon, follow the steps below:
1. **Install Python**:
- Make sure Python is installed. You can download it from https://www.python.org/downloads/
2. **Setup Python Virtual Environment**:
Open your terminal and run the following commands to create a virtual environment:
```bash
python -m venv anon_env
source anon_env/bin/activate # For Linux/Mac
anon_env\Scripts\activate # For Windows
```
3. **Install Required Libraries**:
Install the necessary Python libraries using pip:
```bash
pip install requests stem python-dotenv
```
4. **Tor Installation**:
Ensure Tor is installed and running on your system. You can download it from
https://www.torproject.org/download/.
5. **Proxy Setup in Firefox**:
To use the Tor network in Firefox, follow these steps:
- Open Firefox and go to `Settings`.
- Scroll down to `Network Settings` and click `Settings...`
- Choose `Manual proxy configuration` and set the SOCKS Host to `127.0.0.1` and Port to `9050`.
- Select `SOCKS5` as the proxy type and check `Proxy DNS when using SOCKS v5`.
6. **Set Up Environment Variables**:
Create a `.env` file in the directory where the script is located and add your Tor password like this:
```
TOR_PASSWORD=your_tor_password
```

#How to Use Anon Tool
Once you've set up Anon, follow the steps below to use it for anonymous
browsing:
1. **Activate Virtual Environment**:
Ensure you're in the virtual environment by running:
```bash
source anon_env/bin/activate # For Linux/Mac
anon_env\Scripts\activate # For Windows
```
2. **Run the Tool**:
You can use Anon in either automatic or manual mode:
- **Automatic Mode** (Automatically renew IP every 5 minutes by default):
```bash
python anon.py -m automatic
```
- **Manual Mode** (Renew IP manually when prompted):
```bash
python anon.py -m manual
```
3. **Accessing Dark Web**:
After setting up the proxy in Firefox, you can now use the browser to access
`.onion` websites. Simply open Firefox and enter a `.onion` address to start
browsing anonymously.
