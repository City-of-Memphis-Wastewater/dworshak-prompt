# src/dworshak_prompt/cli.py

import typer
from dworshak_prompt import DworshakPrompt, PromptMode
import os

app = typer.Typer()

@app.command()
def ask(
    mode: str = "console",
    env: str | None = None,
):
    val = DworshakPrompt.ask(
        "Enter value:",
        priority=[PromptMode(mode)],
        debug=True,
    )
    if env and val:
        print(f"export {env}={val}")
        os.environ[env] = val

if __name__ == "__main__":
    app()
