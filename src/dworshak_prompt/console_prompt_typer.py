# src/dworshak_prompt/console_prompt_typer.py
"""
Typer-based console prompt. Non ideal for tty.
"""
from __future__ import annotations
import typer # keep at the top to enable failure, to hit the std lib fallback
from rich.console import Console
import sys
import logging
logger = logging.getLogger(__name__)

# Create a console that specifically targets stderr
stderr_console = Console(stderr=True)

from .keyboard_interrupt import PromptCancelled

def console_get_input_typer(
    message: str, 
    suggestion: str | None = None, 
    hide_input: bool = False,
    default: str | None = None,
    ) -> str | None:
    try:        
            
        if hide_input:
            sgst_msg=""
            if suggestion:
                logger.debug("Credential suggestion not shown in console for security. Please use PromptMode.WEB or PromptMode.GUI to enjoy suggestion autofill for credentials.")
                
                sgst_msg=" (suggestion hidden)"
            hidden_msg = f"{message} (input hidden){sgst_msg}"

            try:
                from rich.prompt import Prompt
                return Prompt.ask(hidden_msg,
                                  password=True,
                                  console=stderr_console)
            except ImportError:
                return typer.prompt(hidden_msg, hide_input=True)
        
        # Standard credential case
        if suggestion: # and not hide_input
            return typer.prompt(
                message,
                default=suggestion)
        return typer.prompt(message)
    except (typer.Abort, KeyboardInterrupt, EOFError, SystemExit):
        # We catch everything Typer/Rich/Python throws on Ctrl+C
        # and raise our own "Hard Stop" signal.
        raise PromptCancelled()
