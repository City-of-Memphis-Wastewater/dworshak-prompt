# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.3.11] - 2026-06-15
### Fixed:
- Path resolution improved.
- Rule: users must provide a filepath for the vault, not just a dir.
- dworshak-secret set to 1.3.5.1

---

## [0.3.10] – 2026-06-05
### Changed:
Ladies and gentlemen, we now have config windows. when force_prompt_is True in obtain_mngr.config() and when the suggestion is the current value from disk (only for plaontext config, not secrets).

### Fixed:
- Actually use force_prompt in obtain.py.

---

## [0.3.9] – 2026-06-04
### Changed:
- Implement new logging approach with logging_setup.configure_logging_for_application(), and in various dependencies.

---

## [0.3.8] – 2026-06-01
### Fixed:
- Guard cryptography import properly in dworshak-secret v1.3.4

---

## [0.3.7] – 2026-06-01
### Fixed:
- '--extra cryptography' corrected to '--extra crypto' in the PYZ build

---

## [0.3.6] – 2026-06-01
### Changed:
- Include typer and cryptography in the PYZ build

---

## [0.3.5] – 2026-06-01
### Changed:
- Web interface now will close smoothly given submit or cancel.
- GUI is working on WSL after I reinstalled my local environment.
- BREAKING: PromptMode.CONSOLE changed to PromptMode.CLI.
- Increase dworshak-secret to 1.3.2

---

## [0.3.4] – 2026-04-20
### Fixed:
- Nested double quotes in multiplexer.py, in two instances of dictionary key reference inside of an f-string. Convert the inner instance to single quotes.

---

## [0.3.3] – 2026-04-10
### Fixed:
- Increase dworshak-secret to 1.2.20, which registers and handles custom .key paths.

---

## [0.3.2] – 2026-04-10
### Fixed:
- setup_dworshak_managers() now references db_path for DworshakSecret properly.
- setup_dworshak_managers() now checks for None before Path() normalization and routes None properly to use the embedded fallbacks (to the %user/.dworshak folder).

---

## [0.3.1] – 2026-04-09
### Changed:
- Update dworshak-prompt to 0.3.1, to mark the mental shift of dworshak-prompt as the programmatic center of the dworshak-ecosystem, becuase:
- dworshak-prompt now offers setup_managers.setup_dworshak_managers()
- Increase `typer-helptree` dependency (in typer extra group), to 0.2.8; leverage this to update the SVG helptree asset.

---

## [0.2.39] – 2026-04-06
### Changed:
- Update dworshak-config to 0.2.6, which now has json healing options.

---

## [0.2.38] – 2026-03-26
### Fixed:
- Increase dworshak-secret to 1.2.16, which resolves import error in backup_vault() function, now in actions.py file.
- Increase pyhabitat to 1.2.6 (which handles the on_termux() function properly for Python 3.13).

---

## [0.2.37] – 2026-03-25
### Fixed:
- Fixed typo in dworshak-env 0.1.7, PACKAGE_NAMW

---

## [0.2.36] – 2026-03-24
### Changed:
- Remove cancel confirm from web interface. The alternative, adjusting the confirm interface buttons, is too complex for maintenance.

---

## [0.2.35] – 2026-03-23
### Fixed:
- Add forget flag to cli.obtain_secret() signature

---

## [0.2.34] – 2026-03-18
### Added:
- InterruptBehavior.RAISE

---

## [0.2.33] – 2026-03-16
### Fixed:
- Verbose and debuf handling move to Obtain class instantiation rather than the functions.

---

## [0.2.32] – 2026-03-16
### Fixed:
- Ensure helptree is updated.
- Ensure examples and docs are consistent with the argument changes from v0.2.31.

---

## [0.2.31] – 2026-03-16
### Changed:
- default_avoid_interface - > interface_avoid
- default_prompt_interface - > interface_prompt
- avoid_interface - > interface_avoid
- prompt_interface - > interface_prompt
- exit_on_interrupt beahvior migrated to instead use 
- interrupt_behavior argument implemeneted, with the InterruptBehavior class.

### Fixed:
- Suggestion, default, and overwrite performance made consistent in Obtain.env(), Obtain.secret(), and Obtain.config(); however, Obtain.secret() differs because the existing value will not be offered as a suggestion.

### Internal:
- Breaking changes will occur in if consuming libraries don't update altered function args.

---

## [0.2.30] – 2026-03-14
### Fixed:
- `from rich import Console` -> `from rich.console import Console`

---

## [0.2.29] – 2026-03-14
### Added:
- `exit_on_interrupt` arg addded to multiplexer.DworshakPrompt.ask() and to the functions which leverage ask():  Obtain.env(), Obtain.config(), Obtain.secret().
- print() message for exit_on_interrupt send to file=sys.stderr

---

## [0.2.28] – 2026-03-09
### Changed:
- obtain=Obtain() available for import in __init__.py
- Lose StoreMode class dworshak_prompt() wrapper. 
- Add self.prompt to Obtain class.

### Internal:
- Consider dropping DWORSHAK_FORCE_INTERACTIVE_TTY to hit TTy for console when wrapped, find a way to make it standard. 


---

## [0.2.27] – 2026-03-08
### Changed:
- Filename change, console_prompt.py -> console_prompt_typer.py
- TTY capture fallback when DWORSHAK_FORCE_INTERACTIVE_TTY=1.
- TRY_TKINTER_ON_WSL -> DWORSHAK_TRY_TKINTER_ON_WSL

---

## [0.2.26] – 2026-03-07
### Changed:
- Increase dworshak-secret to 1.2.15, to guard failure if vault does not exist.
- Message flag stabdardized as not positional, just flag. -m lower case now.
- Update helptree.

---

## [0.2.25] – 2026-03-02
### Changed:
- '--suggestion' flag single char flag changed from '-S' to '-s' for consistency with the wider ecosystem.
- Stabilize stderr vs stdout.
- Increase deps to:
    - dworshak-config==0.2.5
    - dworshak-env==0.1.6
    - dworshak-secret==1.2.14
    - typer-helptree==0.2.6
    
---

## [0.2.24] – 2026-02-28
### Changed:
- Increase dworshak-secret to 0.2.11, where manage-vault -> vault.
- README section about Obtain needs to.show.class instantiation parentheses.

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
