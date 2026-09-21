# AgentO₃ Privacy Gate — Prototype Demo

This directory contains the prototype demonstration for **AgentO₃** (Smart India Hackathon 2026 — Problem Statement 26171: On-device Visual Perception for Light-weight Browser Agents).

The demo showcases how user inputs (Email, Password, Credit Card, Mobile, Face Photo) on an Indian Government-themed web portal are captured locally and sanitized in real-time before reaching the Cloud AI Agent perception view.

---

## 🚀 Quick Start

Run the demo launcher script:

```bash
python tests/run_demo.py
```

### What Happens:
1. Starts the local WebSockets & HTTP server on `http://localhost:8000`.
2. Automatically launches **2 side-by-side browser windows**:
   - **Browser 1 (Left Window)**: `http://localhost:8000/index.html` (User Input Screen)
     - Styled as an official Indian Government Citizen Portal (Sharp edges, emblem, tricolor banner).
     - Contains fields for Full Name, Age, Gender, DOB, Mobile Number, Email Address, Password, Credit Card, and Drag & Drop Photo Upload.
   - **Browser 2 (Right Window)**: `http://localhost:8000/sanitized.html` (Agent Perception View)
     - Live real-time stream receiving user actions.
     - Automatically redacts sensitive PII:
       - Email -> `<user mail>`
       - Password -> `<user pass>`
       - Credit Card -> `<user card>`
       - Mobile Phone -> `<user phone>`
       - Photo -> Applied live Gaussian blur + `<FACE_BLURRED>` watermark.
     - Displays live JSON payload terminal stream sent to the Cloud VLM.

---

## 🛠 File Structure

- `demo_server.py`: Async Python `aiohttp` web server handling static assets and real-time WebSockets broadcasting.
- `run_demo.py`: Playwright orchestration script launching dual tiled Chromium browsers.
- `static/index.html`: User form page styled with official Government of India aesthetics.
- `static/sanitized.html`: Agent perception view showing sanitized DOM and face blurring.
- `static/styles.css`: Sharp-edged official Indian Govt CSS + Agent dark cyber theme.
- `static/user.js`: User input event handlers, image upload, and WebSocket client.
- `static/agent.js`: Agent perception view receiver, canvas image blur engine, and JSON log renderer.
