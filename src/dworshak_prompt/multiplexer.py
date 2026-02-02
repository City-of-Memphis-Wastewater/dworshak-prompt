# src/dworshak_prompt/multiplexer.py
from __future__ import annotations
import typer
import pyhabitat as ph
from enum import Enum
from typing import Set, Any

from .cli_prompt import cli_get_input
from .gui_prompt import gui_get_input
from .web_prompt import web_get_input

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
        force: Set[PromptMode] | None = None,
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
                return DworshakPrompt._handle_cli(message, suggestion, hide_input)
            except (KeyboardInterrupt, EOFError):
                typer.echo("\nInput cancelled.")
                raise PromptCancelled()

        # --- BRANCH 2: GUI ---
        if PromptMode.GUI not in avoid and not ph.on_wsl() and (
            PromptMode.GUI in force or (ph.tkinter_is_available() and not force)
        ):
            try:
                from .guiconfig import gui_get_input # Relative import within lib
                val = gui_get_input(message, hide_input)
                if val is not None: return val
            except Exception:
                # Fallback to Web if GUI fails
                return DworshakPrompt.ask(message, suggestion, hide_input, force, avoid | {PromptMode.GUI}, manager)

        # --- BRANCH 3: WEB ---
        if PromptMode.WEB not in avoid:
            from .config_via_web import browser_get_input
            return browser_get_input(manager=manager, key=message, prompt_message=message, hide_input=hide_input)

        raise RuntimeError("No available prompt mechanism found.")

    @staticmethod
    def _handle_cli(msg: str, suggestion: str | None, hide: bool) -> str:
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