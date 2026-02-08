# src/dworshak_prompt/console_prompt.py
from .keyboard_interrupt import PromptCancelled

def console_get_input(message: str, suggestion: str | None = None, hide_input: bool = False) -> str:
    try:
        import typer
        if hide_input:
            try:
                from rich.prompt import Prompt
                return Prompt.ask(message, password=True)
            except ImportError:
                return typer.prompt(message, hide_input=True)
        
        # Standard credential case
        if suggestion:
            return typer.prompt(message, default=suggestion)
        return typer.prompt(message)
    except (typer.Abort, KeyboardInterrupt, EOFError, SystemExit):
        # We catch everything Typer/Rich/Python throws on Ctrl+C
        # and raise our own "Hard Stop" signal.
        raise PromptCancelled()
