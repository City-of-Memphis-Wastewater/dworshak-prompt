# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.2.19] – 2026-02-14
### Added:
- env command in cli.py
- 'key' keyword used in dworshak-env 0.1.4, rather than 'item' 

### Changed:
- Updates dwroshak ecosystem deps following CLI standardization.
- Deleted dworshak_prompt.py and obtain.py
- Change name of get.py to obtain.py.

---

## [0.2.18] – 2026-02-13
### Internal:
- Release after time delay to allow PyPI to propogate

---

## [0.2.17] – 2026-02-13
### Changed:
- Increase dworshak_config to 0.2.1 ConfigManager - > DworshakConfig
---

## [0.2.16] – 2026-02-13
### Fixed:
- Double dot import error: '.__init__' -> '.'

---

## [0.2.15] – 2026-02-13
### Added:
- dworshak-env

### Changed:
- Set status to beta

---

## [0.2.14] – 2026-02-12
### Added:
- Expose get.py functionality in cli.py. 

### Changed:
- Make typer an optional dependency group.
- Standardized extras to typer and crypto, which is consistent across the dworshak ecosystem.

### Fixed:
- Reference actual dworshak-config package rather than the hardcoded .whl path.

### Changed:
- Make typer an optional dependency group.

---

## [0.2.13] – 2026-02-10
### Changed:
- PromptManager is no longer a singleton but it instantiated per request.

---

## [0.2.12] – 2026-02-10
### Fixed:
- Ensure both imports (DworshakPrompt and PromptMode) are handled under single __getattr__ in __init__.py
- Explicitly define __dir__ to include __all__, along with the pythonic standards.

---

## [0.2.11] – 2026-02-09
### Fixed:
- Default suggestion should be None. It was conflated with the default message.

---

## [0.2.10] – 2026-02-09
### Changed:
- Stop using `bump-my-version` on this project. Pydantic is a cancer and it will not live here.

---

## [0.2.9] – 2026-02-09
### Added:
- Enable cli.py and cli_stdlib.py to use both positional arg for message as well as --message/-M flag.

---

## [0.2.8] – 2026-02-09
- Minor changes, retest

---

## [0.2.7] – 2026-02-09
### Added:
- build_pyz.py; this uses the lite std lib version for console and the cli, so typer is not required.
- .github/workflows/build.yml

---

## [0.2.6] – 2026-02-09
### Changed:
- Alter extra name to be appropriate for differentiating bewtween std lib cli callback and typer optional deps; `cli` extra -> `typer` extra.

### Added:
- Web and GUI prompts now each have a hide/show button, only when the hide arg is True.
- Specify flags in CLI, namely for message and mode.

---

## [0.2.5] – 2026-02-09
### Added:
- Std lib fallback cli and console_prompt features.

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
