# src/dworshak_prompt/get.py
from dworshak_config import ConfigManager
from dworshak_secret import get_secret, store_secret
from .multiplexer import DworshakPrompt

class DworshakGet:
    @staticmethod
    def config(
        service: str, 
        item: str, 
        prompt_message: str | None = None,
        suggestion: str | None = None,
        overwrite: bool = False,
        forget: bool = False,
        timeout: int = 60
    ) -> str | None:
        mgr = ConfigManager()
        value = mgr.get_value(service, item)

        # Logic: If it exists and we aren't forcing a refresh, return it.
        if value is not None and not overwrite:
            return value

        # If missing or overwriting, we use the multiplexer
        # Note: Add your Timeout logic here to wrap the .ask() call
        new_value = DworshakPrompt.ask(
            message=prompt_message or f"[{service}] Enter {item}",
            suggestion=suggestion or value,
            hide_input=False
        )

        # Persistence logic
        if new_value is not None and not forget:
            mgr.set_value(service, item, new_value)
            
        return new_value or value

    @staticmethod
    def secret(service: str, item: str, overwrite: bool = False, timeout: int = 60):
        # Similar logic for secrets, but using dworshak-secret
        value = get_secret(service, item)
        if value is not None and not overwrite:
            return value
            
        new_value = DworshakPrompt.ask(
            message=f"Secret for {service}/{item}",
            hide_input=True
        )
        
        if new_value is not None:
            store_secret(service, item, new_value)
        return new_value