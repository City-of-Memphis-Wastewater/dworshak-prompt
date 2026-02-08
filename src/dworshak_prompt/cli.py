# src/dworshak_prompt/cli.py
import typer
from typer.models import OptionInfo
from rich.console import Console
import os
from .multiplexer import DworshakPrompt, PromptMode
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


if __name__ == "__main__":
    app()
