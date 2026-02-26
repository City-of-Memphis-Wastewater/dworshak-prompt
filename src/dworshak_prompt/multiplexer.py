# src/dworshak_prompt/multiplexer.py
from __future__ import annotations
import pyhabitat as ph
from enum import Enum
from typing import Set, Any
import threading
import traceback
import sys
import os

try:
    from .console_prompt import console_get_input
except ImportError:
    from .console_prompt_stdlib import console_get_input_stdlib as console_get_input
    
from .gui_prompt import get_tkinter_hint
if ph.tkinter_is_available():
    from .gui_prompt import gui_get_input
else:
    gui_get_input = None
from .web_prompt import browser_get_input
from .keyboard_interrupt import PromptCancelled
from .server import stop_prompt_server
from .prompt_manager import PromptManager
from .helpers import PromptMode, resolve_str_to_list, resolve_str_to_set

class DworshakPrompt: 
    def __init__(self,
        config_path: str | None = None,
        secret_path: str | None = None,
        default_priority_interface: list[PromptMode] | None = None,
        default_avoid_interface: set[PromptMode] | None =None,
    ):
        self.config_path = config_path
        self.secret_path = secret_path
        self.default_priority_interface = default_priority_interface
        self.default_avoid_interface = default_avoid_interface

    def ask(
        self,
        message: str = "Enter value",
        suggestion: str | None = None,
        default: Any | None = None,
        hide_input: bool = False, 
        priority_interface: list[PromptMode] | None = None,
        avoid_interface: set[PromptMode] | None = None,
        interrupt_event: threading.Event | None = None,
        debug: bool = False, 
        verbose: bool = False, 
        timeout: int | float | None = None,
    ) -> str | None:
        from .logging_setup import setup_logging
        logger = setup_logging(verbose=verbose, debug=debug, initial=True)

        if priority_interface is None:
            priority_interface = self.default_priority_interface
        if avoid_interface is None:
            avoid_interface = self.default_avoid_interface

        # Use existing interrupt_event or create a local one for this call
        if interrupt_event is None:
            interrupt_event = threading.Event()

        # 1. CI/Headless Detection
        # If we aren't in a TTY and aren't on a system that can spawn a GUI/Web window,
        # return the default immediately to mitigate a potential Dworshak failure mode in CI.
        if ph.is_likely_ci_or_non_interactive():
            logger.debug("CI/Non-interactive environment. Returning default.")
            return default

        if not ph.interactive_terminal_is_available() and \
        not ph.tkinter_is_available() and \
        not ph.is_browser_available(): # Hypothetical pyhabitat check
            logger.debug("Non-interactive environment detected. Using default.")
            return default

        avoid_interface = avoid_interface or set()
        avoid_interface = resolve_str_to_set(avoid_interface)
        priority_interface = resolve_str_to_list(priority_interface)
         
        if ph.on_wsl():
            raw_val = os.getenv("TRY_TKINTER_ON_WSL")
            logger.debug(f"raw TRY_TKINTER_ON_WSL = {raw_val!r}")
            
            # Convert common truthy strings to boolean
            if raw_val is not None:
                try_tkinter_on_wsl = raw_val.lower() in ('1', 'true', 'yes', 'on', 'enable')
            else:
                try_tkinter_on_wsl = False
            
            logger.debug(f"try_tkinter_on_wsl interpreted as {try_tkinter_on_wsl}")
            
            if not try_tkinter_on_wsl:
                logger.warning(f"PromptMode.GUI avoided for WSL; to try it, set `export TRY_TKINTER_ON_WSL=1` ")
                avoid_interface.add(PromptMode.GUI)
                

        default_order = [PromptMode.CONSOLE, PromptMode.GUI, PromptMode.WEB]
        if priority_interface:
            # User choice first, followed by everything else as a safety net
            effective_priority_interface = priority_interface + [m for m in default_order if m not in priority_interface]
        else:
            effective_priority_interface = default_order

        if timeout:
            # A background timer to fire the interrupt signal
            timer = threading.Timer(timeout, lambda: interrupt_event.set())
            timer.start()

        for interface_mode in effective_priority_interface:
            if interface_mode in avoid_interface:
                logger.debug(f"Skipping {interface_mode} (avoided)")
                continue

            logger.debug(f"\n=== Interface Mode: {interface_mode} ===")
            
            try:
                if interface_mode == PromptMode.CONSOLE:
                    if not ph.interactive_terminal_is_available():
                        logger.debug(f"{interface_mode} skipped: No interactive terminal.")
                        continue
                    
                    val = console_get_input(message = message, suggestion = suggestion, hide_input = hide_input)
                    logger.debug(f"SUCCESS: {interface_mode} returned: {repr(val)}")
                    return val

                elif interface_mode == PromptMode.GUI:
                    print(f"ph.tkinter_is_available() = {ph.tkinter_is_available()}")
                    if not ph.tkinter_is_available():
                        logger.warning(f"{interface_mode} skipped: Tkinter unavailable.")
                        logger.debug(get_tkinter_hint())  
                        continue

                        
                    val = gui_get_input(message = message, suggestion = suggestion, hide_input = hide_input)
                    if val is not None:
                        logger.debug(f"SUCCESS: {interface_mode} returned: {repr(val)}")
                        return val
                    
                    logger.debug(f"GUI cancelled. Raising PromptCancelled.")
                    raise PromptCancelled()

                elif interface_mode == PromptMode.WEB:
                    local_manager = PromptManager()
                    try:
                        val = browser_get_input(
                            message, 
                            suggestion, 
                            hide_input, 
                            manager = local_manager, 
                            stop_event = interrupt_event
                            )
                        if val is not None:
                            logger.debug(f"SUCCESS: {interface_mode} returned: {repr(val)}")
                            return val
                        logger.debug(f"WEB returned None. Raising PromptCancelled.")
                        raise PromptCancelled()
                    finally:
                        stop_prompt_server()

            
            except BaseException as e:
                import logging
                exc_type = type(e)
                exc_name = exc_type.__name__
                exc_module = exc_type.__module__
                
                logger.debug(f"!!! EXCEPTION TRIGGERED !!!")
                logger.debug(f"Class Name: {exc_name}")
                logger.debug(f"Full Path:  {exc_module}.{exc_name}")
                logger.debug(f"Repr:       {repr(e)}")
                logger.debug(f"Args:       {e.args}")

                stop_signals = {"KeyboardInterrupt", "Abort", "SystemExit", "EOFError", "PromptCancelled"}
                
                if exc_name in stop_signals or isinstance(e, (KeyboardInterrupt, PromptCancelled)):
                    logger.debug(f">>> MATCHED STOP SIGNAL: {exc_name}. EXITING FUNCTION.")
                    if interrupt_event:
                        interrupt_event.set()
                    return None

                # For technical failures, we log the traceback at DEBUG level
                logger.debug(f">>> TECHNICAL FAILURE detected. Investigating traceback...")
                if logger.isEnabledFor(logging.DEBUG):
                    traceback.print_exc(file=sys.stdout)
                
                logger.debug(f"Continuing to fallback interface mode...")
                continue

            logger.debug("All interface modes exhausted.")
            raise RuntimeError("No input method succeeded.")

def dworshak_ask(
    message: str = "Enter value",
    suggestion: str | None = None,
    default: Any | None = None,
    priority_interface: list[PromptMode] | None = None,
    avoid_interface: set[PromptMode] | None = None,
    **kwargs: Any
) -> str | None:
    """
    Convenience function to prompt the user for input using the Dworshak Multiplexer.
    Automatically handles fallback between Console, GUI, and Web interface modes.
    """
    return DworshakPrompt().ask(
        message=message,
        suggestion=suggestion,
        default=default,
        priority_interface=priority_interface,
        avoid_interface=avoid_interface,
        **kwargs 
    )

# --- Demo entry ---

def main():
    DworshakPrompt().ask(
        "What is your name?",
        suggestion="George",
        debug=True,
    )