# docs/USERS.md 

# DworshakPrompt: User Stories & Vision

DworshakPrompt is designed to reliably capture user input across environments
without requiring developers to build UI or worry about context-specific fallbacks.

---

## User Story 1: CI / Headless Safe

If your code runs in CI pipelines or headless environments, you don’t want to
hang waiting for input. DworshakPrompt returns the `default` immediately if no
interactive input is possible, preventing broken jobs or timeouts.

**Example:**

```python
from dworshak_prompt import DworshakPrompt

env = DworshakPrompt.ask(
    message="Target environment",
    suggestion="production",  # human-facing
    default="staging",        # used in CI or headless
)

```

---

User Story 2: Simple input without building UX

You need credentials, API keys, or basic configuration values quickly. You don’t want to implement a console prompt, GUI, or web interface. DworshakPrompt handles all the interfacing under the hood.

Lightweight scripts that are cross-platform, e.g., pipx-installed tools running on laptops or Termux.

Works out-of-the-box without touching existing GUIs.

Provides an easy, safe, and consistent API for grabbing input.


Example:

```python
from dworshak_prompt import DworshakPrompt

api_key = DworshakPrompt.ask(
    message="Enter API key",
    hide_input=True
)

```

---

User Story 3: Augment existing applications

For heavier applications that already have dedicated interfaces, you may occasionally need special-case input or credentials. Instead of revamping your GUI or building new interaction layers, DworshakPrompt can step in:

Automatically chooses the most appropriate input method.

Skips modes incompatible with the environment.

Integrates seamlessly without modifying your existing codebase.


Example:

```python
from dworshak_prompt import DworshakPrompt, PromptMode

special_secret = DworshakPrompt.ask(
    message="Enter special key",
    priority=[PromptMode.CONSOLE, PromptMode.GUI],
    avoid={PromptMode.WEB},
    hide_input=True
)

```

---

Philosophy

Input is treated as an environment-dependent capability, not a given.

Every input call is resilient: console, GUI, web, or fallback to default.

Designed for developers who want reliability, simplicity, and cross-platform behavior without extra dependencies.


