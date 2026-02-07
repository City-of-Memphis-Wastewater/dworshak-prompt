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

## User Story 2: Simple input without building UX

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

## User Story 3: Augment existing applications

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

## User Story 4: AI / Agent & Multi-User Workflows

When building tools that may be automated or run by multiple agents (e.g., AI assistants, bots, or pipelines), you sometimes need input that is:

Occasionally human-driven

Occasionally automated or non-interactive

Safe to skip or default when unattended


DworshakPrompt handles this automatically:

Returns defaults in non-interactive contexts

Falls back to console, GUI, or web input when available

Can integrate with threads or events for programmatic cancellation


Example:

```python

from dworshak_prompt import DworshakPrompt, PromptMode
import threading

cancel_event = threading.Event()

api_key = DworshakPrompt.ask(
    message="Enter API key for agent workflow",
    suggestion="Use your AI service key",  # human-facing
    default="NONE",                         # safe fallback for automation
    priority=[PromptMode.WEB, PromptMode.CONSOLE],
    hide_input=True,
    interrupt_event=cancel_event,
    debug=True
)

if cancel_event.is_set():
    print("Input cancelled by user or agent")
```

Why this matters:
Your automated workflows can safely handle optional human input without breaking pipelines, hanging scripts, or requiring major changes to existing UIs.


---


Philosophy

Input is treated as an environment-dependent capability, not a given.

Every input call is resilient: console, GUI, web, or fallback to default.

Designed for developers who want reliability, simplicity, and cross-platform behavior without extra dependencies.


