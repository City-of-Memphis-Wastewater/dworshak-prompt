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

class DworshakPrompt__:
    @staticmethod
    def ask(
        message: str,
        suggestion: str | None = None,
        hide_input: bool = False,
        priority: list[PromptMode] | None = None,
        force: Set[PromptMode] | None = None, # possibly remove force arg, in favor of just the priority list
        avoid: Set[PromptMode] | None = None,
        manager: Any | None = None  # Passing the Web Manager through
    ) -> str:
        """
        The 'Monster' Engine: Multi-modal input fallback.
        CLI -> GUI -> Web
        """
        force = set(force or [])
        avoid = set(avoid or [])
        force -= avoid

        # 1. WSL Monkeypatch
        if ph.on_wsl() and PromptMode.GUI not in avoid:
            force.discard(PromptMode.GUI)
            avoid.add(PromptMode.GUI)

        # --- BRANCH 1: CONSOLE ---
        if PromptMode.CONSOLE not in avoid and (
            PromptMode.CONSOLE in force or (ph.interactive_terminal_is_available() and not force)
        ):
            try:
                return cli_get_input(message, suggestion, hide_input)
            except (KeyboardInterrupt, EOFError): # 
                typer.echo("\nInput cancelled.")
                raise PromptCancelled()

        # --- BRANCH 2: GUI ---
        if PromptMode.GUI not in avoid and not ph.on_wsl() and (
            PromptMode.GUI in force or (ph.tkinter_is_available() and not force)
        ):
            try:
                val = gui_get_input(message, hide_input)
                if val is not None: return val
            except Exception:
                # Fallback to Web if GUI fails
                return DworshakPrompt.ask(message, suggestion, hide_input, force, avoid | {PromptMode.GUI}, manager)

        # --- BRANCH 3: WEB ---
        if PromptMode.WEB not in avoid:
            active_manager = manager or get_prompt_manager()
            try:
                val = browser_get_input(active_manager, message, hide_input, interrupt_event)
                return value
            finally:
                # This ensures that as soon as the polling loop finishes (success or cancel),
                # the background server is killed and the port is released.
                stop_prompt_server()
        
        raise RuntimeError("No available prompt mechanism found.")

    @staticmethod
    def cli_get_input(msg: str, suggestion: str | None, hide: bool) -> str:
        if hide:
            try:
                from rich.prompt import Prompt
                return Prompt.ask(msg, password=True)
            except ImportError:
                return typer.prompt(msg, hide_input=True)
        
        # Non-hidden logic
        if suggestion:
            try:
                from rich.prompt import Prompt
                return Prompt.ask(msg, default=suggestion)
            except ImportError:
                return typer.prompt(msg, default=suggestion)
        
        return typer.prompt(msg)

        # ----

        try:
            # 1. CLI Mode (Interactive)
            typer.echo(f"\n --- Use CLI input --- ")
            if hide_input:
                # --- password case ----
                try:
                    from rich.prompt import Prompt
                    def secure_prompt(msg: str) -> str:
                        return Prompt.ask(msg, password=True)
                except ImportError:
                    def secure_prompt(msg: str) -> str:
                        return typer.prompt(msg, hide_input=True)
                value = secure_prompt(prompt_message)
            else:
                # --- credential case ----
                if suggestion:
                    value = typer.prompt(prompt_message, default = suggestion)
                else:
                    value = typer.prompt(prompt_message) 
        except PromptCancelled:
            raise
        except KeyboardInterrupt:
            typer.echo("\nInput cancelled by user.")
            raise
        return value




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
                    # Logic: use provided manager or get/start the local one
                    active_manager = manager or get_prompt_manager()
                    return browser_get_input(active_manager, message, hide_input, interrupt_event)

            except (PromptCancelled, KeyboardInterrupt):
                raise
            except Exception as e:
                continue

        raise RuntimeError("No input method succeeded.")