# src/dworshak_prompt/get.py
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from dworshak_config import ConfigManager

from .multiplexer import DworshakPrompt

class StoreMode(Enum):
    CONFIG = "config"
    SECERT = "secret"
    ENV = "env"


@dataclass
class SecretData:
    value: str = None
    is_new: bool = False

    def __repr__(self):
        # This prevents the secret from appearing if the whole object is printed 
        return f"SecretData(is_new={self.is_new}, value='********')"
    
    def __bool__(self):
        # Allows 'if result:' to check if a value exists
        return self.value is not None

class DworshakObtain:
    def __init__(self,
        config_path: str | Path | None = None,
        secret_path: str | Path | None = None,
    ):
        self.config_path = config_path
        self.secret_path = secret_path

    def config(
        self,
        service: str, 
        item: str, 
        prompt_message: str | None = None,
        path: str | Path | None = None,
        suggestion: str | None = None,
        default: str | None = None,
        overwrite: bool = False,
        forget: bool = False,
        **kwargs # Pass-through for priority, avoid, debug, etc.
    ) -> str | None:
        if path is None:
            path = self.config_path
            
        mgr = ConfigManager(path = path)
        value = mgr.get(service, item)

        # Logic: If it exists and we aren't forcing a refresh, return it.
        if value is not None and not overwrite:
            return value

        # If missing or overwriting, we use the multiplexer
        new_value = DworshakPrompt().ask(
            message=prompt_message or f"config [{service}][{item}]",
            suggestion=suggestion or value,
            hide_input=False,
            **kwargs # Pass-through for priority, avoid, debug, etc.
        )

        # Persistence logic
        if new_value is not None and not forget:
            mgr.set(service, item, new_value)
            
        return new_value or value

    def secret(
        self,
        service: str, 
        item: str, 
        path: str | Path | None = None,
        overwrite: bool = False,
        **kwargs 
        )-> SecretData:

        if path is None:
            path = self.secret_path
            
        try:
            # Lazy Import dworshak_secret here to avoid top-level crashes
            from dworshak_secret import get_secret, store_secret
        except:
            # Trigger the "Lifeboat" redirection error
            from memphisdrip import safe_notify
            from .messages import notify_missing_function_redirect, MSG_CRYPTO_EXTRA
            # We pass a specific context so the user knows why it failed
            full_msg = notify_missing_function_redirect("DworshakGet.secret()") + MSG_CRYPTO_EXTRA
            safe_notify(full_msg)
            raise SystemExit(1)
        
        # Similar logic for secrets, but using dworshak-secret
        value = get_secret(service, item)
        if value is not None and not overwrite:
            return SecretData(value = value, is_new = False)
        print(f"service = {service}")
        print(f"item = {item}")
        new_value = DworshakPrompt().ask(
            message=f"{service} / {item}",
            hide_input=True,
            **kwargs 
        )
        
        if new_value is None:
            # User cancelled (KeyboardInterrupt)
            return SecretData(value=None, is_new=None)
        
        store_secret(service, item, new_value)
        return SecretData(value = new_value, is_new = True)
    

def dworshak_obtain(store: StoreMode = StoreMode.CONFIG,*args,**kwargs):
    if store == StoreMode.CONFIG:
        return DworshakObtain().config(*args,**kwargs)
    elif store == StoreMode.SECRET:
        return DworshakObtain().secret(*args,**kwargs)
    elif store == StoreMode.ENV:
        return DworshakObtain().env(*args,**kwargs)