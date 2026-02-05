# src/dworshak_prompt/cli_prompt.py

import typer

def cli_get_input(message: str, suggestion: str | None = None, hide_input: bool = False) -> str:
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