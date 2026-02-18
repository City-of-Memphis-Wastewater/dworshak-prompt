'# dworshak-prompt

A Python utility that ensures you can always get user input by falling back through multiple interfaces.

### How it works

It captures input by cycling through modes based on environment availability:

1. **Console** (CLI)
2. **GUI** (Tkinter)
3. **Web** (Local Browser Server)

Automatically skips incompatible modes (e.g., GUI on WSL) via `pyhabitat`.


### Usage

### Leverage dworshak-config, dworshak-config, and dworshak-env to handle values

```python
from dworshak_prompt import DworshakObtain

DworshakObtain.config("")
DworshakObtain.secret("")
DworshakObtain.env("")

```

###H Handle values yourself

```python
from dworshak_prompt import DworshakPrompt, PromptMode

# Basic
val = DworshakPrompt().ask("Enter value")

# Options
val = DworshakPrompt().ask(
    message = "Secure Key",
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
val = DworshakPrompt().ask(
    message = "Target Environment",
    suggestion="production",  # What the human sees
    default="staging"         # What the CI/Headless system uses
)
```

Leveraging `dworshak-prompt` for calling and adding configured values.

```python
from dworshak_prompt import DworshakConfig

# Custom path for a specific project
eds_config = DworshakConfig("~/.pipeline-eds/config.json")
api_key = eds_config.get("api_key", message="Enter EDS API Key")
```

The default config file path is "~/.dworshak/config.json".

---

## Install as CLI (for demo purposes)

```bash
pipx install "dworshak-prompt[typer]"
dworshak-prompt --version
dworshak-prompt --help
dworshak-prompt ask --message "Please state name" --mode web
```

---

## Add dworshak-prompt to Python project
When using `uv` for dependency management.
```
uv add dworshak-prompt --extra typer
```

Or, when using raw `pip` for dependency management.
```
pip install "dworshak-prompt[typer]"
``` 

Including the `typer` optional dependency group ensures that Typer and Rich are included as a dependencies. 
Without this, the CLI and console_prompt functionality are still stable, due to Python standard library fallbacks. 

---

## More Information

- [User Stories](https://github.com/City-of-Memphis-Wastewater/dworshak-prompt/blob/main/docs/USERS.md)
