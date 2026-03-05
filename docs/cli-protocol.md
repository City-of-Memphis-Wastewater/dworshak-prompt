## `docs/cli-protocol.md`

# Dworshak CLI Output Protocol

## Overview

To ensure `dworshak-prompt` remains both human-friendly and automation-safe, all CLI commands must adhere to a strict **Stream Separation Contract**. This protocol defines how values, status messages, and diagnostics are routed to the user or the shell.

## 1. The Three Channels

We treat output as three distinct planes. A command's behavior is defined by which plane it is currently addressing.

| Channel | Purpose | Accessibility |
| --- | --- | --- |
| **stdout** | **Data Plane**: Raw values for machine consumption. | Capturable by `$(...)` or pipes. |
| **stderr** | **Human Plane**: Feedback, status, and diagnostics. | Always visible in terminal; does not pollute variables. |
| **tty** | **Interactive Plane**: Live user input (prompts). | Managed by terminal device drivers (e.g., `/dev/tty`). |

---

## 2. Flag Semantics

### `--emit` (The Data Gate)

* **Purpose**: Explicitly permits a value to be written to `stdout`.
* **Behavior**: When present, the raw value is printed to `stdout`. When absent, `stdout` remains empty.
* **Security**: This is the primary safety for secrets. No secret material should ever enter `stdout` without this flag.

### `--verbose` (The Diagnostic Gate)

* **Purpose**: Enables extra human-readable context.
* **Behavior**: Prints detailed metadata (e.g., source of value, service name) to `stderr`.
* **Independence**: Can be used with or without `--emit`. It never affects `stdout`.

---

## 3. Output Requirements

### Value Emission (`stdout`)

If `--emit` is active:

1. Print **only** the raw value.
2. No labels (e.g., `key: value`).
3. No Rich formatting or colors.
4. No status messages.

### Status & Feedback (`stderr`)

Status messages should be provided by default to avoid "silent success," but they must stay off the data plane.

* **Basic Message (Default)**: A concise confirmation (e.g., `Secret known.`).
* **Hint (Default)**: If a value exists but `--emit` is missing, include: `(use --emit to output value)`.
* **Verbose Message**: Detailed info (e.g., `Source: ~/.dworshak/vault.json`).

---

## 4. Expected Behavior Matrix

| Command | Intent | `stdout` | `stderr` |
| --- | --- | --- | --- |
| `get secret` | Simple Check | (empty) | `Secret known. (use --emit to output value)` |
| `get secret --emit` | Variable Capture | `my-password` | `Secret known.` |
| `get secret --verbose` | Inspect Source | (empty) | `Secret known. Source: Vault. (use --emit to output value)` |
| `get secret -ev` | Full Disclosure | `my-password` | `Secret known. Source: Vault.` |

---

## 5. Implementation Rules for Developers

1. **Never** use `print()` for status messages. Use `typer.echo(..., err=True)` or a dedicated `stderr` logger.
2. **Never** use Rich consoles for `stdout` if the output is intended to be a raw value.
3. **Exit Codes**: Return `0` on success (value found/stored) and non-zero on failure or user cancellation.

