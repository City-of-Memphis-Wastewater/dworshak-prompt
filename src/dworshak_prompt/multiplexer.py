# src/dworshak_prompt/multiplexer.py
from __future__ import annotations
import typer
import pyhabitat as ph
from enum import Enum
from typing import Set, Any

from .cli_prompt import cli_get_input
from .gui_prompt import gui_get_input
from .web_prompt import browser_get_input
#from .prompt_manager import PromptManager # Import the manager class for type hinting
from .browser_utils import is_server_running
from .server import (
    run_prompt_server_in_thread, 
    get_prompt_manager, 
    stop_prompt_server
)

class PromptMode(Enum):
    WEB = "web"
    GUI = "gui"
    CONSOLE = "console"

class PromptCancelled(Exception):
    """User explicitly cancelled or interrupted the input."""
    pass


class DworshakPrompt:
    @staticmethod
    def ask(
        message: str,
        suggestion: str | None = None,
        hide_input: bool = False,
        priority: list[PromptMode] | None = None,
        avoid: set[PromptMode] | None = None,
        manager: Any | None = None,
        interrupt_event: threading.Event | None = None
    ) -> str:
        avoid = avoid or set()
        if ph.on_wsl(): avoid.add(PromptMode.GUI)

        effective_priority = priority or [PromptMode.CONSOLE, PromptMode.GUI, PromptMode.WEB]

        for mode in effective_priority:
            if mode in avoid: continue
            
            try:
                if mode == PromptMode.CONSOLE and ph.interactive_terminal_is_available():
                    return cli_get_input(message, suggestion, hide_input)

                if mode == PromptMode.GUI and ph.tkinter_is_available():
                    val = gui_get_input(message, hide_input)
                    if val: return val

                if mode == PromptMode.WEB:
                    active_manager = manager or get_prompt_manager()
                    try:
                        return browser_get_input(active_manager, message, hide_input, interrupt_event)
                    finally:
                        # CRITICAL: Close the server when browser_get_input returns/raises
                        stop_prompt_server()

            except (KeyboardInterrupt, EOFError):
                # If the user hits Ctrl+C, we STOP everything immediately.
                if interrupt_event:
                    interrupt_event.set()
                print("\n[Dworshak] Input cancelled.")
                return None 

            except Exception as e:
                # Only log/continue on legitimate technical failures
                # print(f"DEBUG: {mode} failed: {e}") 
                continue

        raise RuntimeError("No input method succeeded.")