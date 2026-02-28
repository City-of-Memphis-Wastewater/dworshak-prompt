# src/dworshak_prompt/cli.py

"""
"Lazy Loading with Persistence" or a "Configuration Bootstrapper."
Waterfall logic for configuration.
"""
from __future__ import annotations
from .logging_setup import setup_logging
# Initialize logging before anything else
logger=setup_logging(verbose=False, debug=False, initial=True)  # Default off
import typer
from rich.console import Console
import os
from pathlib import Path
from typing import Optional, List
try:
    from typer_helptree import add_typer_helptree
except:
    pass
from . import DworshakPrompt, PromptMode, DworshakObtain

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

@app.command(name = "ask", help = "Simply prompt for an input. Do not check storage, nor store the input value.")
def ask(
    message: str = typer.Argument(
        DEFAULT_PROMPT_MSG, 
        callback=resolve_message,
        help="The prompt message."),
    msg_flag: Optional[str] = typer.Option(
        None, "--message", "-M", 
        help="Flag alias for message."
    ),
    priority_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--interface", "-i",
        help="Preferred input modes in order (repeatable, e.g., --interface gui --interface console)."
    ),
    avoid_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--avoid", "-a",
        help="Input modes to avoid (repeatable, e.g., --avoid web --avoid gui)."
    ),
    suggestion: Optional[str] = typer.Option(
        None, 
        "--suggestion", "-s", 
        help="The user will be suggested this value."),

    hide: bool = typer.Option(False, "--hide", "-H", help="Hide input (for passwords)"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable low-level diagnostics and tracebacks."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages (recommended).")
    
):

    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None

    """Get user input and print it to stdout."""
    val = DworshakPrompt().ask(
        message=message,
        priority_interface=priority_interface_list,
        avoid_interface=avoid_interface_set,
        suggestion = suggestion,
        hide_input = hide,
        debug=debug, 
        verbose=verbose,
    )
    if val:
        print(val)


# Create the 'obtain' sub-app
obtain_app = typer.Typer(help="If a value cannot be retrieved, it will be prompted for and set.")
app.add_typer(obtain_app, name="obtain")

@obtain_app.command(name="secret", help = "Obtain a secret value (Check Vault -> Prompt -> Save).")
def obtain_secret(
    service: str = typer.Argument(..., help="The service name (e.g., maxson-eds)."),
    item: str = typer.Argument(..., help="The item key (e.g., port)."),
    path: Path = typer.Option(None, "--path","-p", help="Custom encrypted database file path."),
    message: Optional[str] = typer.Option(None, "--message", "-M", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-S", help="Suggested value."),
    priority_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--interface", "-i",
        help="Preferred input modes in order (repeatable, e.g., --interface gui --interface console)."
    ),
    avoid_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--avoid", "-a",
        help="Input modes to avoid (repeatable, e.g., --avoid web --avoid gui)."
    ),
    overwrite: bool = typer.Option(False, "--overwrite/--no-overwrite", help="Force a new prompt."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable low-level diagnostics and tracebacks."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages (recommended).")
):
    """Obtain a secret value (Check Vault -> Prompt -> Save)."""

    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None
    
    result = DworshakObtain(secret_path=path).secret(
        service=service,
        item=item,
        message=message,
        suggestion=suggestion,
        priority_interface=priority_interface_list, 
        avoid_interface=avoid_interface_set, 
        overwrite=overwrite,
        debug=debug,
        verbose=verbose,
    )
    if result.is_new is True:
        print("Secret stored.")
    elif result.is_new is False:
        print("Secret known.")
    elif result.is_new is None:
        print("Exited.")

@obtain_app.command(name="config", help = "Obtain a config value (Check config file -> Prompt -> Save).")
def obtain_config(
    service: str = typer.Argument(..., help="The service name (e.g., maxson-eds)."),
    item: str = typer.Argument(..., help="The item key (e.g., port)."),
    path: Path = typer.Option(None, "--path","-p", help="Custom config file path."),
    message: Optional[str] = typer.Option(None, "--message", "-M", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-S", help="Suggested value."),
    priority_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--interface", "-i",
        help="Preferred input modes in order (repeatable, e.g., --interface gui --interface console)."
    ),
    avoid_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--avoid", "-a",
        help="Input modes to avoid (repeatable, e.g., --avoid web --avoid gui)."
    ),
    overwrite: bool = typer.Option(False, "--overwrite/--no-overwrite", help="Force a new prompt."),
    forget: bool = typer.Option(False, "--forget", help="Don't save the prompted value."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable low-level diagnostics and tracebacks."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages (recommended).")
):
    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None

    """Get a configuration value (Storage -> Prompt -> Save)."""
    val = DworshakObtain(config_path=path).config(
        service=service,
        item=item,
        message=message,
        suggestion=suggestion,
        overwrite=overwrite,
        priority_interface=priority_interface_list,
        avoid_interface=avoid_interface_set,
        forget=forget,
        debug=debug,
        verbose=verbose
    )
    if val:
        print(val)

@obtain_app.command(name="env", help = "Obtain an app setting (Check .env file -> Prompt -> Save).")
def obtain_env(
    key: str = typer.Argument(..., help="The value key (e.g., API_URL)."),
    path: Path = typer.Option(None, "--path","-p", help="Custom .env file path."),
    message: Optional[str] = typer.Option(None, "--message", "-M", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-S", help="Suggested value."),
    priority_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--interface", "-i",
        help="Preferred input modes in order (repeatable, e.g., --interface gui --interface console)."
    ),
    avoid_interface: Optional[List[PromptMode]] = typer.Option(
        None, "--avoid", "-a",
        help="Input modes to avoid (repeatable, e.g., --avoid web --avoid gui)."
    ),
    overwrite: bool = typer.Option(False, "--overwrite/--no-overwrite", help="Force a new prompt."),
    forget: bool = typer.Option(False, "--forget", help="Don't save the prompted value."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable low-level diagnostics and tracebacks."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages (recommended).")
):
    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None

    """Retrieve a setting; falls back to interactive setup if the key is undefined."""
    val = DworshakObtain(env_path=path).env(
        key = key,
        message=message,
        suggestion=suggestion,
        overwrite=overwrite,
        priority_interface=priority_interface_list,
        avoid_interface=avoid_interface_set,
        forget=forget,
        debug=debug,
        verbose=verbose
    )
    if val:
        print(val)


if __name__ == "__main__":
    app()

