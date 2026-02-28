# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.2.24] – 2026-02-28
### Changed:
- Increase dworshak-secret to 0.2.11, where manage-vault -> vault.
- README section about DworshakObtain needs to.show.class instantiation parentheses.

### Added:
- README section for the typer-helptree.

### Fixed:
- Add commas to __all__ in __init__.py, so that dir(dworshak_prompt) is accurate.

---

## [0.2.23] – 2026-02-27
### Changed:
- PromptManager -> PromptManagerWeb; prompt_manager.py -> prompt_manager_web.py
- Update dworshak-env to 0.1.5, dworshak-config to 0.2.4.

### Fixed:
- `--debug` -> `--debug/-d` consistently.
- `--verbose` -> `--verbose/-v` consistently.

### Added:
- Add `--path/-p` cli flag to obtain commands, to allow users to specify non-default paths.
- Descriptions for obtain subcommmands.
- Improve cryptography messaging to encourge user to set up venv with access to system site packages 

### Internal:
- Updates have been made in and dworshak-env, dworshak-config; update these before tagging dworshak-prompt v0.2.23.

---

## [0.2.22] – 2026-02-26
### Fixed:
- Handling the TRY_TKINTER_ON_WSL env var

---

## [0.2.21] – 2026-02-23
### Changed:
- priority -> priorty_interface, PromptMode -> PromptMode, avoid -> avoid_interface

### Added:
- Add cancel button to web interface.
- Add messages for missing tkinter functionality.
- Dedicated logging_setup module (WIP)

### Internal:
- To add logger to a file, use `logger = logging.getLogger("dworshak_prompt")`
- For --debug flag, use logger.debug()
- For --verbose flag, use logger.info()
- For no flag, use logger.warning()

### Fixed:
- Bring cli_stdlib.py into (lite) parallel with cli.py; why the heck are we doing this? Because it is likely the only entry point that will live on in fifty years, if someone can't find the right typer wheel (typer will probably live too, but all bets are off).

---

## [0.2.20] – 2026-02-17
### Changed:
- Increase dworshak-secret to 1.2.8 which now handles:
    - 'Overwite' arg
    - Optional custom vault pathing
    - Has the DworshakSecret class (in parallel with the DworshakEnv and DworshakConfig classes in their respective libraries) 

---

## [0.2.19] – 2026-02-14
### Added:
- env command in cli.py
- 'key' keyword used in dworshak-env 0.1.4, rather than 'item' 

### Changed:
- Updates dworshak ecosystem deps following CLI standardization.
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
- PromptManagerWeb is no longer a singleton but it instantiated per request.

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
