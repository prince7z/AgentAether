import subprocess
import sys
import time
import os
from playwright.sync_api import sync_playwright

def run_demo():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(base_dir, "demo_server.py")

    print("================================================================")
    print(" AgentO3 Prototype Demo — Real-Time Privacy Redaction Gate")
    print("================================================================")
    print("[1/3] Starting local HTTP & WebSocket server on http://localhost:8000 ...")

    # Launch server as a background subprocess
    server_process = subprocess.Popen([sys.executable, server_script, "8000"])
    
    # Allow server to initialize
    time.sleep(1.5)

    print("[2/3] Launching dual browser windows (Side-by-Side) ...")
    print("  -> Browser 1 (Left):  User Input Form (Gov of India Theme)")
    print("  -> Browser 2 (Right): Agent Perception View (Sanitized Live)")

    with sync_playwright() as p:
        # Browser 1: User Screen on Left Side
        browser1 = p.chromium.launch(
            headless=False,
            args=[
                '--window-position=0,0',
                '--window-size=920,980'
            ]
        )
        page1 = browser1.new_page()
        page1.goto('http://localhost:8000/index.html')

        # Browser 2: Agent Perception Screen on Right Side
        browser2 = p.chromium.launch(
            headless=False,
            args=[
                '--window-position=930,0',
                '--window-size=920,980'
            ]
        )
        page2 = browser2.new_page()
        page2.goto('http://localhost:8000/sanitized.html')

        print("[3/3] Prototype Demo Active! Type or upload images in Browser 1.")
        print("Press Ctrl+C in this terminal window to stop the demo server.")

        try:
            while True:
                time.sleep(0.5)
                if not browser1.is_connected() or not browser2.is_connected():
                    break
        except KeyboardInterrupt:
            print("\nShutting down AgentO3 demo...")
        finally:
            try:
                browser1.close()
            except:
                pass
            try:
                browser2.close()
            except:
                pass
            server_process.terminate()
            print("Demo shutdown complete.")

if __name__ == "__main__":
    run_demo()
