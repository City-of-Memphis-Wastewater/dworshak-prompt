# src/dworshak_prompt/cli.py
import typer
from typer.models import OptionInfo
from rich.console import Console
import os
from pathlib import Path

from .multiplexer import DworshakPrompt, PromptMode 
from .dworshak_config import ConfigManager
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

@app.command()
def ask(
    message: str = typer.Option("Enter value", help="The prompt message."),
    mode: PromptMode = typer.Option(default = PromptMode.CONSOLE, help="Preferred input mode."),
    debug: bool = typer.Option(False, "--debug", help="Enable diagnostic logging."),
):
    """Get user input and print it to stdout."""
    val = DworshakPrompt.ask(
        message=message,
        priority=[mode],
        debug=debug, 
    )
    if val:
        print(val)


@app.command()
def config(
    service: str = typer.Argument(..., help="The service name (e.g., Maxson)."),
    item: str = typer.Argument(..., help="The item key (e.g., port)."),
    value: str = typer.Option(None, "--set", help="Directly set a value."),
    message: str = typer.Option(None, "--message", help="Custom prompt message."),
    path: Path = typer.Option(None, "--path", help="Custom config file path."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt."),
    hide: bool = typer.Option(False, "--hide", help="Mask input for sensitive info."),
):
    """
    Get or set a configuration value using Service and Item (Vault-style).
    """
    manager = ConfigManager(path=path)
    
    if value is not None:
        manager.set_value(service, item, value)
        display_val = "***" if hide else value
        typer.echo(f"Stored: [{service}] {item} = {display_val}")
    else:
        result = manager.get(
            service=service,
            item=item,
            prompt_message=message,
            overwrite=overwrite,
            hide_input=hide
        )
        if result:
            # Only print the result to stdout for piping/capture
            print(result)

if __name__ == "__main__":
    app()

