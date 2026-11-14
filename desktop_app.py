"""
TKIET EduPlan Desktop Application Launcher
Runs the platform as a standalone native desktop application window.
"""

import sys
import os
import time
import subprocess
import webbrowser

def launch():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_dir, "app.py")
    
    print("=" * 60)
    print("  Starting TKIET EduPlan AI - Standalone Desktop App")
    print("=" * 60)

    # 1. Start Streamlit in background headless mode
    server_cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.headless=true",
        "--server.port=8501"
    ]
    
    proc = subprocess.Popen(server_cmd, cwd=base_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    url = "http://localhost:8501"
    
    # 2. Try launching as dedicated native app window (no address bar, no tabs)
    # Check for Edge (default on Windows 10/11)
    edge_paths = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        "msedge"
    ]
    
    launched = False
    for ep in edge_paths:
        try:
            subprocess.Popen([ep, f"--app={url}", "--window-size=1280,820"])
            launched = True
            break
        except Exception:
            continue

    if not launched:
        # Check Chrome
        chrome_paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            "chrome"
        ]
        for cp in chrome_paths:
            try:
                subprocess.Popen([cp, f"--app={url}", "--window-size=1280,820"])
                launched = True
                break
            except Exception:
                continue

    if not launched:
        webbrowser.open(url)

    print("\nDesktop Application window is running.")
    print("Close the desktop window or press Ctrl+C here to stop.")
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()

if __name__ == "__main__":
    launch()
