# dworshak-prompt

A Python utility that ensures you can always get user input by falling back through multiple interfaces.
`dworshak-prompt` is a CI-safe, shell-friendly prompting engine that integrates with persistent config and secret storage.

### How it works

It captures input by cycling through modes based on environment availability:

1. **Console** (CLI)
2. **GUI** (Tkinter)
3. **Web** (Local Browser Server)

Automatically skips incompatible modes (e.g., GUI on WSL) via `pyhabitat`.


### Usage

### Obtain
Leverage dworshak-config, dworshak-config, and dworshak-env to automatically handle values.

```python
from dworshak_prompt import Obtain

obtain = Obtain()

obtain.config(service, item, message)
obtain.secret(service, item, message)
obtain.env(key, message)

```

### Ask

Prompt the user then handle values manually.

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
from dworshak_prompt import Obtain, PromptMode, InterruptBehavior, 

# Identify custom path for a specific project, and set defaults during instantiation of the Obtain class.
obtain_mgr = Obtain(
    config_path="~/.pipeline-eds/config.json"
    interface_priority = [PromptMode.GUI, PromptMode.WEB]
    interface_avoid = {PromptMode.CONSOLE}
    interrupt_behavior = InterruptBehavior.EXIT,
    debug = True
    )
api_key = obtain_mgr.config("api_key", message="Enter EDS API Key")
```

The default config file path is "~/.dworshak/config.json".

---

## CLI

The [dworshak](https://github.com/City-of-Memphis-Wastewater/dworshak) layer is the intended primary CLI entry point, but the `dworshak-prompt` CLI can be used directly.

```bash
pipx install "dworshak-prompt[typer]"
dworshak-prompt --version
dworshak-prompt --help
dworshak-prompt ask --message "Please state name" --interace web
```

`dworshak-prompt` is designed to be useful even without Python code. 
It can be used directly from shell scripts, CI pipelines, and ops tooling to safely obtain, persist, and reuse configuration values.

Piping and environment variable capture works, but will naturally fallback to GUI or Web input because in these cases `stdout` is not a TTY. However, you may continue to use console input and leverage `dev/tty` by using envionrmental variable `DWORSHAK_FORCE_INTERACTIVE_TTY`.

```zsh
# Enable console input during wrapped or piped shell capture.
export DWORSHAK_FORCE_INTERACTIVE_TTY=1
VAR=$(dworshak-prompt obtain secret "special_api" "password" --emit)
```

See the `dworshak-prompt` Typer CLI structure.
```
dworshak-prompt helptree
```

<p align="center">
  <img src="https://raw.githubusercontent.com/City-of-Memphis-Wastewater/dworshak-prompt/main/assets/dworshak-prompt_v0.2.31_helptree.svg" width="100%" alt="Screenshot of the dworshak-prompt CLI helptree">
</p>

`helptree` is utility funtion for Typer CLIs, imported from the `typer-helptree` library.

- GitHub: https://github.com/City-of-Memphis-Wastewater/typer-helptree
- PyPI: https://pypi.org/project/typer-helptree/

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
Without this, the CLI and console prompting functionality are still stable, due to Python standard library fallbacks. 

---

## More Information

- [User Stories](https://github.com/City-of-Memphis-Wastewater/dworshak-prompt/blob/main/docs/USERS.md)

---

## Sister Projects in the Dworshak Ecosystem

* **CLI/Orchestrator:** [dworshak](https://github.com/City-of-Memphis-Wastewater/dworshak)
* **Interactive UI:** [dworshak-prompt](https://github.com/City-of-Memphis-Wastewater/dworshak-prompt)
* **Secrets Storage:** [dworshak-secret](https://github.com/City-of-Memphis-Wastewater/dworshak-secret)
* **Plaintext Pathed Configs:** [dworshak-config](https://github.com/City-of-Memphis-Wastewater/dworshak-config)
* **Classic .env Injection:** [dworshak-env](https://github.com/City-of-Memphis-Wastewater/dworshak-env)

```bash
pipx install dworshak
pip install dworshak-secret
pip install dworshak-config
pip install dworshak-env
pip install dworshak-prompt

```
