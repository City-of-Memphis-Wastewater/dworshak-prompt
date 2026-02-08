# src/dworshak_prompt/dworshak_config.py
from pathlib import Path
import json
import logging
from typing import Any
from .multiplexer import DworshakPrompt

logger = logging.getLogger("dworshak_prompt")

DEFAULT_CONFIG_PATH = Path.home() / ".dworshak" / "config.json"
class ConfigManager:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else DEFAULT_CONFIG_PATH

    def _load(self) -> dict:
        """Loads the nested JSON config."""
        if not self.path.exists():
            return {}
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"⚠️ Warning: Config file '{self.path}' is corrupted: {e}")
            return {}

    def _save(self, config: dict):
        """Saves the nested JSON config."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logger.error(f"⚠️ Failed to save configuration to {self.path}: {e}")

    def get(
        self,
        service: str,
        item: str,
        prompt_message: str | None = None,
        suggestion: str | None = None,
        overwrite: bool = False,
        hide_input: bool = False,
        forget: bool = False,
    ) -> str | None:
        """Retrieves a value using service/item logic, prompting if missing."""
        config = self._load()
        
        # Access nested: config[service][item]
        service_dict = config.get(service, {})
        value = service_dict.get(item)

        if value is not None and not overwrite:
            return value

        # If we need to prompt
        actual_prompt = prompt_message or f"[{service}] Enter {item}"
        
        new_value = DworshakPrompt.ask(
            message=actual_prompt,
            suggestion=suggestion or value,
            hide_input=hide_input
        )

        if new_value is None:
            return value if not overwrite else None

        if not forget:
            if service not in config:
                config[service] = {}
            config[service][item] = new_value
            self._save(config)
            
        return new_value

    def set_value(self, service: str, item: str, value: Any):
        """Directly sets a nested value."""
        config = self._load()
        if service not in config:
            config[service] = {}
        config[service][item] = value
        self._save(config)