"""
Docstring for dworshak_prompt.dworshak_config

Vars:
- path to configuration file
    - defaults to .dworshak/config.json
    - can be specified by any program that consumes the dwroshak-prompt library to point to a package specific path, like ~/.pipeline-eds/config.json

"""
from pathlib import Path
import logging
import sys
import pyhabitat as ph
import json

# Setup logger
logger = logging.getLogger("dworshak_prompt")
# Default to INFO to hide diagnostics; change to DEBUG to see them
#logger.setLevel(logging.INFO) 
logger.setLevel(logging.WARNING) 
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(_handler)

DEFAULT_CONFIG_FILE = Path.home() / ".dworshak" / "config.json"

from pathlib import Path
import json
import logging
import sys
from typing import Any
import pyhabitat as ph
from .multiplexer import DworshakPrompt

logger = logging.getLogger("dworshak_prompt")

class ConfigManager:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else Path.home() / ".dworshak" / "config.json"

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"⚠️ Warning: Config file '{self.path}' is corrupted: {e}")
            # Here you could implement your json_heal logic
            return {}

    def _save(self, config: dict):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logger.error(f"⚠️ Failed to save configuration to {self.path}: {e}")

    def get(
        self,
        key: str,
        prompt_message: str | None = None,
        suggestion: str | None = None,
        overwrite: bool = False,
        forget: bool = False,
    ) -> str | None:
        config = self._load()
        value = config.get(key)

        # Logic: If we have it and aren't forcing an overwrite, return it
        if value is not None and not overwrite:
            return value

        # If we need to prompt
        actual_prompt = prompt_message or f"Enter value for '{key}'"
        
        # Use the existing DworshakPrompt multiplexer
        new_value = DworshakPrompt.ask(
            message=actual_prompt,
            suggestion=suggestion or value, # Use existing as suggestion if overwriting
        )

        if new_value is None:
            return value if not overwrite else None

        if not forget:
            config[key] = new_value
            self._save(config)
            
        return new_value