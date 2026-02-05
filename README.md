# dworshak-prompt

A Python utility that ensures you can always get user input by falling back through multiple interfaces.

### How it works

It captures input by cycling through modes based on environment availability:

1. **Console** (CLI)
2. **GUI** (Tkinter)
3. **Web** (Local Browser Server)

Automatically skips incompatible modes (e.g., GUI on WSL) via `pyhabitat`.

### Usage

```python
from dworshak_prompt import DworshakPrompt, PromptMode

# Basic
val = DworshakPrompt.ask("Enter value")

# Options
val = DworshakPrompt.ask(
    "Secure Key",
    hide_input=True,
    priority = [PromptMode.CONSOLE, PromptMode.GUI]
    avoid = {PromptMode.WEB}

)

```

Another example, for handling CI:

```python
from dworshak_prompt import DworshakPrompt, PromptMode

# If this runs in GitHub Actions, it returns "staging" immediately.
# If it runs on a laptop, it pops up a GUI or Console prompt.
val = DworshakPrompt.ask(
    "Target Environment",
    suggestion="production",  # What the human sees
    default="staging"         # What the CI/Headless system uses
)
```