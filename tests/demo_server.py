import asyncio
import json
import os
import sys
from aiohttp import web

# Path to static assets directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Connected WebSocket clients
ws_clients = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ws_clients.add(ws)
    print(f"[Server] Client connected. Total clients: {len(ws_clients)}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = msg.data
                # Broadcast payload to all other connected clients
                for client in list(ws_clients):
                    if client != ws and not client.closed:
                        await client.send_str(data)
            elif msg.type == web.WSMsgType.ERROR:
                print(f"[Server] WebSocket error: {ws.exception()}")
    finally:
        ws_clients.remove(ws)
        print(f"[Server] Client disconnected. Total clients: {len(ws_clients)}")
    return ws

async def init_app():
    app = web.Application()
    app.router.add_get('/ws', websocket_handler)
    
    # Custom handler for index and sanitized pages
    async def handle_index(request):
        return web.FileResponse(os.path.join(STATIC_DIR, "index.html"))

    async def handle_sanitized(request):
        return web.FileResponse(os.path.join(STATIC_DIR, "sanitized.html"))

    app.router.add_get('/', handle_index)
    app.router.add_get('/index.html', handle_index)
    app.router.add_get('/sanitized.html', handle_sanitized)
    
    # Static files directory
    app.router.add_static('/', path=STATIC_DIR, name='static')
    return app

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    app = asyncio.run(init_app())
    print(f"==================================================")
    print(f" AgentO3 Demo Server starting on http://localhost:{port}")
    print(f" User Form:      http://localhost:{port}/index.html")
    print(f" Agent View:     http://localhost:{port}/sanitized.html")
    print(f"==================================================")
    web.run_app(app, host="127.0.0.1", port=port)
