import os
import sys
import time
from pathlib import Path

import requests

# Reconfigure stdout to handle unicode prints safely on Windows terminal
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

# Add project root to path so 'app' can be imported when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Load local environment variables from .env file
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip().strip("'\"")

# from app.tools.sandbox.commands import (  # noqa: E402
#     start_sandbox_server,
#     stop_sandbox_server,
# )

# config = {"configurable": {"thread_id": "tg-1833617010"}}

# print("Stopping any existing server on port 3000...")
# print(stop_sandbox_server.invoke({"port": 3000}, config=config))

# print("Starting server on port 3000...")
# print(
#     start_sandbox_server.invoke(
#         {
#             "get_preview": True,
#             "port": 3000,
#             "command": "cd /workspace/react-app && npm start",
#         },
#         config=config,
#     )
# )

# print("Waiting 15s for React dev server to finish compiling...")
# time.sleep(15)

# headers = {"Ngrok-Skip-Browser-Warning": "true"}
# response = requests.get(
#     "https://nonadeptly-subconsular-verdie.ngrok-free.dev",
#     headers=headers,
#     verify=False,
# )
# print("Preview Response:", response)
# print("Status Code:", response.status_code)

from app.agent.planner import llm_with_tools

# res=llm_with_tools.invoke("Hello, how are you?")
# print(res)

import json

tools = llm_with_tools.kwargs.get("tools", [])

print("\n" + "=" * 80)
print(f"🔧 BOUND TOOLS: {len(tools)}")
print("=" * 80)

for i, tool in enumerate(tools, 1):
    fn = tool.get("function", {})

    serialized = json.dumps(tool, ensure_ascii=False)

    print(
        f"{i:02d}. {fn.get('name'):30} "
        f"{len(serialized):5} chars"
    )

print("=" * 80)