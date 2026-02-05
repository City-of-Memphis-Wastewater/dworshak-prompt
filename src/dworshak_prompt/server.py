# src/dworshak_prompt/server.py
from __future__ import annotations
import http.server
import socketserver
import json
import urllib.parse
import threading
from .browser_utils import find_open_port

# Shared state between the HTTP thread and the Multiplexer thread
from .prompt_manager import get_prompt_manager

class PromptHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silence the console noise

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)

        if parsed_url.path == "/config_modal":
            self._serve_html(params)
        elif parsed_url.path == "/api/get_active_prompt":
            self._serve_json(get_prompt_manager().get_active_prompt())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/submit_config":
            # 1. Determine how much data to read
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "Empty submission")
                return

            # 2. Read and parse the URL-encoded form data
            post_data = self.rfile.read(content_length).decode('utf-8')
            fields = urllib.parse.parse_qs(post_data)
            
            # 3. Extract our specific fields
            req_id = fields.get('request_id', [None])[0]
            val = fields.get('input_value', [None])[0]

            if req_id and val is not None:
                # --- THE HANDOFF ---
                manager = get_prompt_manager()
                manager.submit_result(req_id, val) 
                # -------------------
                
                self._send_response("<h1>Success</h1><p>Input received. You may now close this tab.</p>")
            else:
                self.send_error(400, "Missing request_id or input_value")
        else:
            self.send_error(404)

    def _serve_html(self, params):
        req_id = params.get('request_id', [''])[0]
        msg = params.get('message', ['Input Required'])[0]
        
        # Inlined HTML to keep it zero-dep and avoid resource-loading drama
        html = f"""<!DOCTYPE html>
        <html>
        <head><title>Prompt</title><style>
            body {{ font-family: sans-serif; padding: 20px; background: #f0f2f5; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            input {{ width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }}
            button {{ background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }}
        </style></head>
        <body>
            <div class="card">
                <h2>{msg}</h2>
                <form action="/api/submit_config" method="post">
                    <input type="hidden" name="request_id" value="{req_id}">
                    <input type="text" name="input_value" autofocus required>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body></html>"""
        self._send_response(html, "text/html")

    def _send_response(self, content, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _serve_json(self, data):
        self._send_response(json.dumps(data or {"show": False}), "application/json")

def run_prompt_server_in_thread(port=8083):
    port = find_open_port(port)
    # ThreadingMixIn allows multiple requests (like the HTML page + the JSON poll)
    class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    httpd = ThreadedServer(("127.0.0.1", port), PromptHandler)
    get_prompt_manager().set_server_host_port(f"127.0.0.1:{port}")
    
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return thread