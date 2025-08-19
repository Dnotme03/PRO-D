import os
import sys
import subprocess
import logging
import time

# ---------------- Auto-install modules ----------------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from flask import Flask, send_from_directory
except ModuleNotFoundError:
    print("Installing Flask...")
    install("flask")
    from flask import Flask, send_from_directory

try:
    from pyngrok import ngrok
except ModuleNotFoundError:
    print("Installing pyngrok...")
    install("pyngrok")
    from pyngrok import ngrok

# ---------------- Terminal colors ----------------
RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
CYAN = '\033[1;36m'
RESET = '\033[0m'

# ---------------- Suppress Flask logs ----------------
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# ---------------- Clear terminal & banner ----------------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{RED}
██████╗ ██████╗  ██████╗     
██╔══██╗██╔══██╗██╔═══██╗    
██████╔╝██████╔╝██║   ██║    
██╔═══╝ ██╔═══╝ ██║   ██║    
██║     ██║     ╚██████╔╝    
╚═╝     ╚═╝      ╚═════╝     
{CYAN}Professional Python Server{RESET}""")
    print(f"{YELLOW}Made by: Your Dev Friend{RESET}\n")

# ---------------- Flask setup ----------------
app = Flask(__name__)
selected_html = "1.html"

@app.route('/')
def home():
    return send_from_directory(".", selected_html)

# ---------------- Run ----------------
if __name__ == "__main__":
    banner()

    # Choose template
    choice = input(f"{YELLOW}Choose Page Template [1/2]: {RESET}").strip()
    selected_html = "1.html" if choice == "1" else "2.html"

    # Server port
    port = 8080

    # Start ngrok tunnel
    print(f"{CYAN}Starting public tunnel via ngrok...{RESET}")
    public_url = ngrok.connect(port)
    print(f"{GREEN}Public URL is ready: {public_url}{RESET}")
    print(f"{GREEN}Local URL: http://127.0.0.1:{port}{RESET}")

    # Run Flask
    app.run(host="127.0.0.1", port=port, debug=False)
