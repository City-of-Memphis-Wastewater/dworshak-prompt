# src/dworshak_prompt/cli.py
import typer
#$from typer.models import OptionInfo
from rich.console import Console
import os
from pathlib import Path
from typing import Optional
from typer_helptree import add_typer_helptree
from memphisdrip import typer_resolve_arg_flag_pair

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

# In cli.py
add_typer_helptree(app=app, console=console, version = __version__,hidden=True)

@app.command()
def ask(
    message: str = typer.Argument(
        DEFAULT_PROMPT_MSG, 
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
    
    message = typer_resolve_arg_flag_pair(message, msg_flag, default = DEFAULT_PROMPT_MSG)

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
    #service: str = typer.Argument(..., help="Service name."),
    #item: str = typer.Argument(..., help="Key name."),
    service: Optional[str] = typer.Argument(None, help="Service name."),
    item: Optional[str] = typer.Argument(None, help="Key name."),
    service_flag: Optional[str] = typer.Option(None, "--service", "-s", help="Flag alias for service name."),
    item_flag: Optional[str] = typer.Option(None, "--item", "-i", help="Flag alias for item key."),
    message: Optional[str] = typer.Option(None, "--message", "-M", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-S", help="Suggested value."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt."),
    forget: bool = typer.Option(False, "--forget", help="Don't save the prompted value."),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    service = typer_resolve_arg_flag_pair(service, service_flag)
    item = typer_resolve_arg_flag_pair(item, item_flag)

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
    #service: str = typer.Argument(..., help="Service name."),
    #item: str = typer.Argument(..., help="Key name."),
    #service: Optional[str] = typer.Argument(None, help="Service name."),
    #item: Optional[str] = typer.Argument(None, help="Key name."),
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Flag alias for service name."),
    item: Optional[str] = typer.Option(None, "--item", "-i", help="Flag alias for item key."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt."),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    """Get a secret value (Vault -> Prompt -> Save)."""

    #service = typer_resolve_arg_flag_pair(None, service_flag)
    #item = typer_resolve_arg_flag_pair(None, item_flag)

    # If the user didn't provide them via flags, prompt for them right now.
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

