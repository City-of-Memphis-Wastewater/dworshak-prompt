# src/dworshak_prompt/browser_utils.py
from __future__ import annotations 
import os
import shutil
import subprocess
import time
import socket
import webbrowser
import urllib.request
import urllib.error


def launch_browser(url: str):
    """Refined, silent WSLg-aware launcher."""
    # 1. Termux
    if shutil.which("termux-open-url"):
        subprocess.Popen(["termux-open-url", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    # 2. WSLg / Edge (The 'Muzzle' logic)
    edge_bin = shutil.which("microsoft-edge")
    if edge_bin:
        env = os.environ.copy()
        # Force basic (non-keyring) storage to prevent the keyring password popup
        env["PYTHON_KEYRING_BACKEND"] = "keyring.backends.null.Keyring" 
        env["PASSWORD_STORE"] = "basic"

        # Try to quiet down excessive console prints for chromium launch in WSL
        env["CHROME_LOG_LEVEL"] = "3"
        log_path = os.path.expanduser("~/.cache/dworshak_browser.log")
        if os.path.exists(log_path) and os.path.getsize(log_path) > 10 * 1024 * 1024:
            open(log_path, 'w').close()
        env["CHROME_LOG_FILE"] = log_path

        with open(os.devnull, 'w') as fnull:
            subprocess.Popen(
                [edge_bin, url, "--no-first-run", "--quiet", "--disable-gpu", 
                 "--disable-dev-shm-usage", "--remote-debugging-port=0"],
                stdout=fnull, stderr=fnull, env=env, start_new_session=True
            )
        return
    # Try general Linux desktop launcher
    if shutil.which("xdg-open"):
        env = os.environ.copy()
        # Force basic (non-keyring) storage to prevent the keyring password popup
        env["PYTHON_KEYRING_BACKEND"] = "keyring.backends.null.Keyring" 
        env["PASSWORD_STORE"] = "basic"
        try:
            print("[WEBPROMPT] Attempting launch using 'xdg-open'...")
            subprocess.Popen(
                ["xdg-open", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env = env
            )
            launched = True
            return
        except FileNotFoundError:
            pass # shutil.which should prevent this, so we silently fall through
        except Exception as e:
            print(f"[WEBPROMPT WARNING] 'xdg-open' failed: {e}. Falling back...")

    # 3. Fallback
    webbrowser.open_new_tab(url)

def find_open_port(start: int = 8082, end: int = 8100) -> int:
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start

def is_server_running(url: str) -> bool:
    """Check if server is up using stdlib only."""
    try:
        # We use a short timeout because it's localhost
        with urllib.request.urlopen(url, timeout=0.5) as response:
            return response.getcode() < 500
    except (urllib.error.URLError, TimeoutError, ConnectionRefusedError):
        return False
    except Exception:
        return False