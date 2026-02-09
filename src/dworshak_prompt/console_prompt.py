# src/dworshak_prompt/console_prompt.py
import typer # keep at the top to enable failure, to hit the std lib fallback

from .keyboard_interrupt import PromptCancelled

def console_get_input(message: str, suggestion: str | None = None, hide_input: bool = False) -> str:
    try:        
        if hide_input:
            # Explicitly add the hint so the user isn't confused by lack of feedback
            hidden_msg = f"{message} (input hidden)"
            try:
                from rich.prompt import Prompt
                return Prompt.ask(hidden_msg, password=True)
            except ImportError:
                return typer.prompt(hidden_msg, hide_input=True)
        
        # Standard credential case
        if suggestion: # and not hide_input
            return typer.prompt(message, default=suggestion)
        return typer.prompt(message)
    except (typer.Abort, KeyboardInterrupt, EOFError, SystemExit):
        # We catch everything Typer/Rich/Python throws on Ctrl+C
        # and raise our own "Hard Stop" signal.
        raise PromptCancelled()
