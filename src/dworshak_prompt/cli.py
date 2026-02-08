# src/dworshak_prompt/cli.py

import typer
from typer.models import OptionInfo
from rich.console import Console
import os

from .multiplexer import DworshakPrompt, PromptMode
from ._version import get_version, __version__


console = Console() # to be above the tkinter check, in case of console.print
app = typer.Typer()

# Force Rich to always enable colors, even when running from a .pyz bundle
os.environ["FORCE_COLOR"] = "1"
# Optional but helpful for full terminal feature detection
os.environ["TERM"] = "xterm-256color"

app = typer.Typer(
    name="dwroshak-prompt",
    help=f"Multiplexed user input via console, GUI, and web, depending on availability. (v{__version__})",
    add_completion=False,
    invoke_without_command = True,
    no_args_is_help = True,
    context_settings={"ignore_unknown_options": True,
                      "allow_extra_args": True,
                      "help_option_names": ["-h", "--help"]},
)

@app.command()
def ask(
    mode: str = "console",
    env: str | None = None,
):
    val = DworshakPrompt.ask(
        "Enter value",
        priority=[PromptMode(mode)],
        debug=True,
    )
    if env and val:
        print(f"export {env}={val}")
        os.environ[env] = val

if __name__ == "__main__":
    app()
