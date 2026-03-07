/# src/dworshak_prompt/cli.py

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
from . import DworshakPrompt, PromptMode, Obtain

from ._version import __version__


console = Console() # to be above the tkinter check, in case of console.print
app = typer.Typer()

# Force Rich to always enable colors, even when running from a .pyz bundle
os.environ["FORCE_COLOR"] = "1"
# Optional but helpful for full terminal feature detection
os.environ["TERM"] = "xterm-256color"

DEFAULT_PROMPT_MSG = "Enter value"

# --- helper ---

def finalize_protocol_output(
    value: Optional[str],
    emit: bool,
    verbose: bool,
    status_msg: str,
    v_msg: Optional[str] = None
):
    # 1. Human Plane (stderr)
    if status_msg:
        typer.echo(f"[*] {status_msg}", err=True)

    if verbose and v_msg:
        typer.echo(f"VERBOSE: {v_msg}", err=True)

    # 2. Data Plane (stdout)
    if value is not None:
        if emit:
            # Raw output for redirection
            # Use sys.stdout.write(value) if you want to avoid the trailing newline
            typer.echo(value)
        else:
            typer.echo("(use --emit to emit value)", err=True)
    else:
        # If we expected a value but got None, signal failure to the shell
        if emit:
            typer.echo("Error: No value to emit.", err=True)
            raise typer.Exit(code=1)

# --- app ---
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

@app.command(name = "ask", help = "Simply prompt for an input. Do not check storage, nor store the input value.")
def ask(
    message: Optional[str] = typer.Option(
        None, "--message", "-m", 
        help="Optional prompt message."
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
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages, to stderr (recommended)."),
    emit:  bool = typer.Option(False, "--emit", "-e", help="Emit value to stdout.")
):

    if message is None:
        message = DEFAULT_PROMPT_MSG
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

    status = "Input captured." if val else "No input received."
    finalize_protocol_output(val, emit, verbose, status)

# Create the 'obtain' sub-app
obtain_app = typer.Typer(help="If a value cannot be retrieved, it will be prompted for and set.")
app.add_typer(obtain_app, name="obtain")

@obtain_app.command(name="secret", help = "Obtain a secret value (Check Vault -> Prompt -> Save).")
def obtain_secret(
    service: str = typer.Argument(..., help="The service name (e.g., maxson-eds)."),
    item: str = typer.Argument(..., help="The item key (e.g., port)."),
    path: Path = typer.Option(None, "--path","-p", help="Custom encrypted database file path."),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-s", help="Suggested value."),
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
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages (recommended)."),
    emit:  bool = typer.Option(False, "--emit", "-e", help="Emit value to stdout.")
):
    """Obtain a secret value (Check Vault -> Prompt -> Save)."""

    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None
    
    result = Obtain(secret_path=path).secret(
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

    finalize_protocol_output(result.value, emit, verbose, result.status_message)

@obtain_app.command(name="config", help = "Obtain a config value (Check config file -> Prompt -> Save).")
def obtain_config(
    service: str = typer.Argument(..., help="The service name (e.g., maxson-eds)."),
    item: str = typer.Argument(..., help="The item key (e.g., port)."),
    path: Path = typer.Option(None, "--path","-p", help="Custom config file path."),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-s", help="Suggested value."),
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
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages (recommended)."),
    emit:  bool = typer.Option(False, "--emit", "-e", help="Emit value to stdout")
):
    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None

    """Get a configuration value (Storage -> Prompt -> Save)."""
    result = Obtain(config_path=path).config(
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
    #status = f"Config '{item}' resolved." if val else "Config not found."
    #v_info = f"Path: {path or 'default'}"
    #finalize_protocol_output(val, emit, verbose, status, v_info)

    finalize_protocol_output(result.value, emit, verbose, result.status_message)
    
    
    
@obtain_app.command(name="env", help = "Obtain an app setting (Check .env file -> Prompt -> Save).")
def obtain_env(
    key: str = typer.Argument(..., help="The value key (e.g., API_URL)."),
    path: Path = typer.Option(None, "--path","-p", help="Custom .env file path."),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="Custom prompt message."),
    suggestion: Optional[str] = typer.Option(None, "--suggestion", "-s", help="Suggested value."),
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
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages (recommended)."),
    emit:  bool = typer.Option(False, "--emit", "-e", help="Emit value to stdout")
):
    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None

    """Retrieve a setting; falls back to interactive setup if the key is undefined."""
    result = Obtain(env_path=path).env(
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

    #status = f"Env var '{key}' resolved." if val else f"'{key}' not set."
    #v_info = f"Searching .env at: {path or os.getcwd()}"
    #finalize_protocol_output(val, emit, verbose, status, v_info)
    finalize_protocol_output(result.value, emit, verbose, result.status_message)

if __name__ == "__main__":
    app()

