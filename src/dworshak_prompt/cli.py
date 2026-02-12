# src/dworshak_prompt/cli.py
import typer
#$from typer.models import OptionInfo
from rich.console import Console
import os
from pathlib import Path
from typing import Optional
from typer_helptree import add_typer_helptree

from .multiplexer import DworshakPrompt, PromptMode 
from .get import DworshakGet

from ._version import __version__


console = Console() # to be above the tkinter check, in case of console.print
app = typer.Typer()

# Force Rich to always enable colors, even when running from a .pyz bundle
os.environ["FORCE_COLOR"] = "1"
# Optional but helpful for full terminal feature detection
os.environ["TERM"] = "xterm-256color"

app = typer.Typer(
    name="dworshak-prompt",
    help=f"Multiplexed user input via console, GUI, and web. (v{__version__})",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"ignore_unknown_options": True,
                      "help_option_names": ["-h", "--help"]},
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

# In cli.py
add_typer_helptree(app=app, console=console, version = __version__,hidden=True)

# This is the "hidden" state to store the flag value
_message_from_flag = None
def message_callback(value: str):
    """
    If the user uses -M or --message, this captures it.
    """
    global _message_from_flag
    if value:
        _message_from_flag = value
    return value

@app.command()
def ask(
    message: str = typer.Argument(
        "Enter value", 
        help="The prompt message."),
    msg_flag: Optional[str] = typer.Option(
        None, "--message", "-M", 
        callback=message_callback, 
        is_eager=True, # Processes this before other arguments
        help="Flag alias for message."
    ),
    mode: PromptMode = typer.Option( 
        PromptMode.CONSOLE,
        "--mode", "-m", 
        help="Preferred input mode."),
    suggestion: Optional[str] = typer.Option(
        None, 
        "--suggestion", "-s", 
        help="The user will be suggested this value."),
    hide: bool = typer.Option(False, "--hide", "-H", help="Hide input (password mode)"),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    
    # If the callback caught a flag value, use it. Otherwise, use the positional.
    final_message = _message_from_flag or message

    """Get user input and print it to stdout."""
    val = DworshakPrompt.ask(
        message=final_message,
        priority=[mode],
        suggestion = suggestion,
        hide_input = hide,
        debug=debug, 
    )
    if val:
        print(val)


# Create the 'get' sub-app
get_app = typer.Typer(help="Retrieve values from config or secrets.")
app.add_typer(get_app, name="get")

@get_app.command(name="config")
def get_config(
    service: str = typer.Argument(..., help="Service name."),
    item: str = typer.Argument(..., help="Key name."),
    message: Optional[str] = typer.Option(None, "--message", "-M", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-s", help="Suggested value."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt."),
    forget: bool = typer.Option(False, "--forget", help="Don't save the prompted value."),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    """Get a configuration value (Storage -> Prompt -> Save)."""
    val = DworshakGet.config(
        service=service,
        item=item,
        prompt_message=message,
        suggestion=suggestion,
        overwrite=overwrite,
        forget=forget,
        debug=debug
    )
    if val:
        print(val)

@get_app.command(name="secret")
def get_secret(
    service: str = typer.Argument(..., help="Service name."),
    item: str = typer.Argument(..., help="Key name."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt."),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    """Get a secret value (Vault -> Prompt -> Save)."""
    val = DworshakGet.secret(
        service=service,
        item=item,
        overwrite=overwrite,
        debug=debug
    )
    if val:
        print(val)


if __name__ == "__main__":
    app()

