# src/dworshak_prompt/cli.py
import typer
#$from typer.models import OptionInfo
from rich.console import Console
import os
from pathlib import Path
from typing import Optional
try:
    from typer_helptree import add_typer_helptree
except:
    pass
from .multiplexer import DworshakPrompt, PromptMode 
from .get import DworshakGet

from ._version import __version__


console = Console() # to be above the tkinter check, in case of console.print
app = typer.Typer()

# Force Rich to always enable colors, even when running from a .pyz bundle
os.environ["FORCE_COLOR"] = "1"
# Optional but helpful for full terminal feature detection
os.environ["TERM"] = "xterm-256color"

DEFAULT_PROMPT_MSG = "Enter value"

app = typer.Typer(
    name="dworshak-prompt",
    help=f"Multiplexed user input via console, GUI, and web. (v{__version__})",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"ignore_unknown_options": True,
                      "help_option_names": ["-h", "--help"]},
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
    version: Optional[bool] = typer.Option(
    None, "--version", is_flag=True, help="Show the version."
    )
    ):
    """
    Enable --version
    """
    if version:
        typer.echo(__version__)
        raise typer.Exit(code=0)

try:
    add_typer_helptree(app=app, console=console, version = __version__,hidden=True)
except:
    pass

def resolve_message(ctx: typer.Context, value: str):
    # ctx.params will already contain 'msg_flag' because Options are parsed first
    msg_flag = ctx.params.get("msg_flag")
    # Priority: 1. Flag, 2. Positional (if not the default), 3. Default
    if msg_flag:
        return msg_flag
    return value

@app.command()
def ask(
    message: str = typer.Argument(
        DEFAULT_PROMPT_MSG, 
        callback=resolve_message,
        help="The prompt message."),
    msg_flag: Optional[str] = typer.Option(
        None, "--message", "-M", 
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

    """Get user input and print it to stdout."""
    val = DworshakPrompt.ask(
        message=message,
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
def get_or_set_config(
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Service name."),
    item: Optional[str] = typer.Option(None, "--item", "-i", help="Item key."),
    message: Optional[str] = typer.Option(None, "--message", "-M", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-S", help="Suggested value."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt."),
    forget: bool = typer.Option(False, "--forget", help="Don't save the prompted value."),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    # If the user didn't provide values via flags, prompt for them now.
    if not service:
        # this is just typer.prompt()
        service = DworshakPrompt.ask("Service name", avoid = {PromptMode.WEB, PromptMode.GUI})
    if not item:
        item = DworshakPrompt.ask("Item key", avoid = {PromptMode.WEB, PromptMode.GUI})

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
def get_or_set_secret(
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Service name."),
    item: Optional[str] = typer.Option(None, "--item", "-i", help="Item key."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt."),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    """Get a secret value (Vault -> Prompt -> Save)."""


    # If the user didn't provide values via flags, prompt for them now.
    if not service:
        service = DworshakPrompt.ask("Service name", avoid = {PromptMode.WEB, PromptMode.GUI})
    if not item:
        item = DworshakPrompt.ask("Item key", avoid = {PromptMode.WEB, PromptMode.GUI})
    
    # If they cancelled the prompt, exit gracefully
    if not service or not item:
        raise typer.Exit(1)
    
    result = DworshakGet.secret(
        service=service,
        item=item,
        overwrite=overwrite,
        debug=debug
    )
    if result.is_new is True:
        print("Secret stored.")
    elif result.is_new is False:
        print("Secret known.")
    elif result.is_new is None:
        print("Exited.")

if __name__ == "__main__":
    app()

