# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.2.4] – 2026-02-08
### Added:
- Add app entry point to pyproject.toml to ensure CLI availability
- README section for pipx installation, specifically clarifying the `[cli]` extra.
- README section for `uv add`, specifically clarifying the `--extra cli` extra.

---

## [0.2.3] – 2026-02-08
### Added:
- Stabilize cli.py as entry point as as example.

### Changed:
- Filename change, cli_prompt.py -> console_prompt.py
- Optional dependency group 'cli' now contains typer and rich, so that web and tkinter can be used without needing to carry those deps.

---

## [0.2.2] – 2026-02-07
### Fixed:
- Improve pyproject.toml description.

---

## [0.2.1] – 2026-02-07
### Added:
- Reference user stories at docs/USERS.md

### Internal:
- Stable usage in pipeline-eds.

---

## [0.1.5] – 2026-02-06
### Fixed:
- Guard tkinter import in gui stuff
- Guard init
- demo, main()

---

## [0.1.4] – 2026-02-06
### Added:
- DworshakPrompt known to __init__

---

## [0.1.3] – 2026-02-06
### Added:
- Initial release to PyPI via publish.yml
