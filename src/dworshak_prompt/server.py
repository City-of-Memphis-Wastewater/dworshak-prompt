# src/dworshak_prompt/server.py
from __future__ import annotations
import msgspec.json
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import HTMLResponse, Response
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import uvicorn
import threading
import time
import urllib.parse
from importlib import resources

from .prompt_manager import PromptManager
from .browser_utils import find_open_port

# --- 1. Global State within the Library Scope ---
_prompt_manager = PromptManager()

def get_prompt_manager() -> PromptManager:
    return _prompt_manager

# --- 2. Middleware (CORS for potential iframe/cross-port embedding) ---
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
]

# --- 3. Route Handlers ---

async def serve_config_modal_html(request: Request):
    """Serves the prompt UI, injecting the request_id and metadata."""
    request_id = request.query_params.get("request_id")
    message = request.query_params.get("message", "Input Required")
    hide_input = request.query_params.get("hide_input", "false").lower() == "true"

    if not request_id:
        raise HTTPException(status_code=400, detail="Missing request_id")

    try:
        # Resolve template from WITHIN dworshak_prompt package
        # Assumes: src/dworshak_prompt/templates/config_modal.html
        html_content = resources.read_text('dworshak_prompt.templates', 'config_modal.html')

        # Injecting values (using simple string replacement to avoid Jinja2 dependency)
        final_html = html_content.replace('{{ request_id }}', urllib.parse.quote_plus(request_id))
        final_html = final_html.replace('{{ message }}', message)
        final_html = final_html.replace('{{ hide_input }}', str(hide_input).lower())

        return HTMLResponse(content=final_html, status_code=200)

    except Exception as e:
        return HTMLResponse(f"<h1>Internal Template Error</h1><p>{e}</p>", status_code=500)

async def get_active_prompt(request: Request):
    """API for the frontend to poll for the current prompt status."""
    manager: PromptManager = get_prompt_manager()
    data = manager.get_active_prompt() # Should return dict with message, hide_input, etc.

    if data:
        data["show"] = True
        return Response(content=msgspec.json.encode(data), media_type="application/json")

    return Response(content=msgspec.json.encode({"show": False}), media_type="application/json")

async def submit_config(request: Request):
    """Receives the user input and unblocks the multiplexer thread."""
    manager: PromptManager = get_prompt_manager()
    try:
        form_data = await request.form()
        request_id = form_data.get("request_id")
        submitted_value = form_data.get("input_value")

        if not request_id or submitted_value is None:
            raise HTTPException(status_code=400, detail="Invalid submission")

        manager.submit_result(request_id, submitted_value)
        return HTMLResponse("<h1>Input Received. You can close this tab.</h1>", status_code=200)
    except Exception as e:
        return HTMLResponse(f"<h1>Submission Error</h1><p>{e}</p>", status_code=500)

# --- 4. App & Lifecycle ---

routes = [
    Route("/config_modal", endpoint=serve_config_modal_html, methods=["GET"]),
    Route("/api/get_active_prompt", endpoint=get_active_prompt, methods=["GET"]),
    Route("/api/submit_config", endpoint=submit_config, methods=["POST"]),
]

app = Starlette(debug=False, middleware=middleware, routes=routes)

def run_prompt_server_in_thread(host: str = "127.0.0.1", port: int = 8083) -> threading.Thread:
    """Launches the server in a daemon thread so it doesn't block the CLI/Multiplexer."""
    
    # Ensure we use an open port
    actual_port = find_open_port(port, port + 50)
    host_port_str = f"{host}:{actual_port}"
    
    # Update manager so browser_get_input knows where to point the browser
    _prompt_manager.set_server_host_port(host_port_str)

    config = uvicorn.Config(app, host=host, port=actual_port, log_level="error")
    server = uvicorn.Server(config=config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for server to bind
    time.sleep(0.4)
    return thread