# src/dworshak_prompt/web_prompt.py
from __future__ import annotations 
import threading
import urllib.parse 
from typing import Any

from .prompt_manager import PromptManager # for type hinting
from .browser_utils import launch_browser, is_server_running

def browser_get_input(message: str, suggestion: str | None = None, hide: bool = False, manager: PromptManager = None, stop_event: threading.Event | None = None) -> str | None:
    
    req_id = manager.register_prompt("input_key", message, hide, suggestion=suggestion)
    url = manager.get_server_url()

    # Launch logic remains the same
    if not is_server_running(url):
        from .server import run_prompt_server_in_thread
        run_prompt_server_in_thread()
        url = manager.get_server_url()

    encoded_msg = urllib.parse.quote_plus(message)
    encoded_sug = urllib.parse.quote_plus(suggestion or "")
    full_url = f"{url}/config_modal?request_id={req_id}&message={encoded_msg}&hide_input={hide}&suggestion={encoded_sug}"
    launch_browser(full_url)

    # The Polling Loop
    while True:
        # 1. Check if the external shutdown event was triggered
        if stop_event and stop_event.is_set():
            manager.clear_result(req_id)
            return None
            
        # 2. Check if the user submitted data
        val = manager.get_and_clear_result(req_id)
        if val is not None:
            return val

        # 3. Responsive Sleep: wait for the event OR the timeout
        # This makes Ctrl+C feel instant
        if stop_event:
            if stop_event.wait(timeout=0.5):
                return None
        else:
            import time
            time.sleep(0.5)