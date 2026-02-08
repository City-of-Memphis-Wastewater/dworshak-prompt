# src/dworshak_prompt/multiplexer.py
from __future__ import annotations
import pyhabitat as ph
from enum import Enum
from typing import Set, Any
import threading
import traceback
import sys
import logging

from .console_prompt import console_get_input
if ph.tkinter_is_available():
    from .gui_prompt import gui_get_input
else:
    gui_get_input = None
from .web_prompt import browser_get_input
from .keyboard_interrupt import PromptCancelled
from .server import (
    get_prompt_manager,
    stop_prompt_server
)


    
# Setup logger
logger = logging.getLogger("dworshak_prompt")
# Default to INFO to hide diagnostics; change to DEBUG to see them
logger.setLevel(logging.INFO) 
#logger.setLevel(logging.DEBUG) 
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(_handler)


class PromptMode(Enum):
    WEB = "web"
    GUI = "gui"
    CONSOLE = "console"

class DworshakPrompt:
    @staticmethod
    def ask(
        message: str,
        suggestion: str | None = None,
        default: Any | None = None,
        hide_input: bool = False,
        priority: list[PromptMode] | None = None,
        avoid: set[PromptMode] | None = None,
        manager: Any | None = None,
        interrupt_event: threading.Event | None = None,
        debug: bool = False  # Added a flag to toggle at runtime
    ) -> str | None:
        if debug:
            logger.setLevel(logging.DEBUG)

        # 1. CI/Headless Detection
        # If we aren't in a TTY and aren't on a system that can spawn a GUI/Web window,
        # return the default immediately to avoid the "Time Bomb."
        if not ph.interactive_terminal_is_available() and \
        not ph.tkinter_is_available() and \
        not ph.is_browser_available(): # Hypothetical pyhabitat check
            logger.debug("[DIAGNOSTIC] Non-interactive environment detected. Using default.")
            return default

        avoid = avoid or set()
        if ph.on_wsl():
            avoid.add(PromptMode.GUI)

        effective_priority = priority or [PromptMode.CONSOLE, PromptMode.GUI, PromptMode.WEB]

        for mode in effective_priority:
            if mode in avoid:
                logger.debug(f"[DIAGNOSTIC] Skipping {mode} (avoided)")
                continue

            logger.debug(f"\n[DIAGNOSTIC] === Entering Mode: {mode} ===")
            
            try:
                if mode == PromptMode.CONSOLE:
                    if not ph.interactive_terminal_is_available():
                        logger.debug(f"[DIAGNOSTIC] {mode} skipped: No interactive terminal.")
                        continue
                    
                    val = console_get_input(message, suggestion, hide_input)
                    logger.debug(f"[DIAGNOSTIC] SUCCESS: {mode} returned: {repr(val)}")
                    return val

                elif mode == PromptMode.GUI:
                    if not ph.tkinter_is_available():
                        logger.debug(f"[DIAGNOSTIC] {mode} skipped: Tkinter unavailable.")
                        continue
                        
                    val = gui_get_input(message, suggestion, hide_input)
                    if val is not None:
                        logger.debug(f"[DIAGNOSTIC] SUCCESS: {mode} returned: {repr(val)}")
                        return val
                    
                    logger.debug(f"[DIAGNOSTIC] GUI cancelled. Raising PromptCancelled.")
                    raise PromptCancelled()

                elif mode == PromptMode.WEB:
                    active_manager = manager or get_prompt_manager()
                    try:
                        val = browser_get_input(message, suggestion, hide_input, active_manager, interrupt_event)
                        if val is not None:
                            logger.debug(f"[DIAGNOSTIC] SUCCESS: {mode} returned: {repr(val)}")
                            return val
                        logger.debug(f"[DIAGNOSTIC] WEB returned None. Raising PromptCancelled.")
                        raise PromptCancelled()
                    finally:
                        stop_prompt_server()

            except BaseException as e:
                exc_type = type(e)
                exc_name = exc_type.__name__
                exc_module = exc_type.__module__
                
                logger.debug(f"[DIAGNOSTIC] !!! EXCEPTION TRIGGERED !!!")
                logger.debug(f"[DIAGNOSTIC] Class Name: {exc_name}")
                logger.debug(f"[DIAGNOSTIC] Full Path:  {exc_module}.{exc_name}")
                logger.debug(f"[DIAGNOSTIC] Repr:       {repr(e)}")
                logger.debug(f"[DIAGNOSTIC] Args:       {e.args}")

                stop_signals = {"KeyboardInterrupt", "Abort", "SystemExit", "EOFError", "PromptCancelled"}
                
                if exc_name in stop_signals or isinstance(e, (KeyboardInterrupt, PromptCancelled)):
                    logger.debug(f"[DIAGNOSTIC] >>> MATCHED STOP SIGNAL: {exc_name}. EXITING FUNCTION.")
                    if interrupt_event:
                        interrupt_event.set()
                    return None

                # For technical failures, we log the traceback at DEBUG level
                logger.debug(f"[DIAGNOSTIC] >>> TECHNICAL FAILURE detected. Investigating traceback...")
                if logger.isEnabledFor(logging.DEBUG):
                    traceback.print_exc(file=sys.stdout)
                
                logger.debug(f"[DIAGNOSTIC] Continuing to fallback mode...")
                continue

        logger.debug("[DIAGNOSTIC] All modes exhausted.")
        raise RuntimeError("No input method succeeded.")

def main():
    DworshakPrompt.ask(
        "What is your name?",
        suggestion="George",
        debug=True,
    )
