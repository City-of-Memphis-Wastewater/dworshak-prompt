# src/dworshak_prompt/get.py
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any
import sys

from dworshak_config import DworshakConfig
from dworshak_env import DworshakEnv
from .multiplexer import DworshakPrompt

class StoreMode(Enum):
    CONFIG = "config"
    SECRET = "secret"
    ENV = "env"


@dataclass
class SecretData:
    """
    Container for secret retrieval results. 
    The __repr__ ensures secrets don't leak into logs/consoles if the object is printed.
    """
    value: Optional[str] = None
    is_new: Optional[bool] = False

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
        env_path: str | Path | None = None,
    ):
        self.config_path = config_path
        self.secret_path = secret_path
        self.env_path = env_path

    def ask(self, *args, **kwargs):
        """Proxy to the multiplexer for direct questions."""
        return DworshakPrompt(
            config_path=self.config_path, 
            secret_path=self.secret_path
        ).ask(*args, **kwargs)
    
    def config(
        self,
        service: str, 
        item: str, 
        message: str | None = None,
        suggestion: str | None = None,
        default: Any | None = None,
        path: str | Path | None = None,
        overwrite: bool = False,
        forget: bool = False,
        **kwargs # Pass-through for priority, avoid, debug, etc.
    ) -> str | None:
        if path is None:
            path = self.config_path
            
        config_mgr = DworshakConfig(path = path)
        value = config_mgr.get(service, item)

        # Logic: If it exists and we aren't forcing a refresh, return it.
        if value is not None and not overwrite:
            return value

        # If missing or overwriting, we use the multiplexer
        new_value = DworshakPrompt().ask(
            message=message or f"config [{service}][{item}]",
            suggestion=suggestion or value,
            hide_input=False,
            **kwargs # Pass-through for priority, avoid, debug, etc.
        )

        # Persistence logic
        if new_value is not None and not forget:
            config_mgr.set(service, item, new_value, overwrite=overwrite)
            
        return new_value if new_value is not None else value

    def secret(
        self,
        service: str, 
        item: str, 
        message: str | None = None,
        suggestion: str | None = None,
        default: Any | None = None,
        path: str | Path | None = None,
        overwrite: bool = False,
        forget: bool = False,
        **kwargs 
        )-> SecretData:

        if path is None:
            path = self.secret_path
            
        try:
            # Lazy Import dworshak_secret here to avoid top-level crashes
            import cryptography
            from dworshak_secret import get_secret, store_secret
        except:
            # Trigger the "Lifeboat" redirection error
            from memphisdrip import safe_notify
            from .messages import notify_missing_function_redirect, MSG_CRYPTO_EXTRA
            # We pass a specific context so the user knows why it failed
            full_msg = notify_missing_function_redirect("DworshakObtain.secret()") + MSG_CRYPTO_EXTRA
            safe_notify(full_msg)
            raise SystemExit(1)
        
        # Similar logic for secrets, but using dworshak-secret
        value = get_secret(service, item)
        if value is not None and not overwrite:
            return SecretData(value = value, is_new = False)
        
        new_value = DworshakPrompt().ask(
            message=message or f"{service} / {item}",
            hide_input=True,
            **kwargs 
        )
        
        if new_value is None:
            # User cancelled (KeyboardInterrupt)
            return SecretData(value=None, is_new=None)
        
        if not forget:
            store_secret(service, item, new_value, overwrite=overwrite)
        return SecretData(value = new_value, is_new = True)
    
    def env(
        self, 
        key: str, 
        message: str | None = None,
        suggestion: str | None = None,
        default: Any | None = None,
        path: str | Path | None = None,
        overwrite: bool = False,
        forget: bool = False,
        **kwargs
    ) -> str | None:
        """
        Checks key from os.environ or .env file, using the dworshak-env library. 
        Prompts user if not found or overwrite is True.
        """
        if path is None:
            path = self.env_path # Defaults to None, DworshakEnv handles Path(".env")

        env_mgr = DworshakEnv(path=path)
        value = env_mgr.get(key)

        # Logic: If it exists and we aren't forcing a refresh, return it.
        if value is not None and not overwrite:
            return value

        # If missing or overwriting, we use the multiplexer
        new_value = DworshakPrompt().ask(
            message=message or f"env [{key}]",
            suggestion=value or default,
            hide_input=False,
            **kwargs
        )

        # Persistence logic: Save to .env file if not forgotten
        if new_value is not None and not forget:
            env_mgr.set(key, new_value, overwrite=overwrite)
            return new_value

        return new_value if new_value is not None else value

def dworshak_obtain(
    service_or_key: str,
    item: str | None = None,
    store: StoreMode = StoreMode.CONFIG,
    message: str | None = None,
    suggestion: str | None = None,
    default: Any | None = None,
    **kwargs
) -> Any:
    """
    Functional entry point for the Obtain engine.
    Allows for one-liner access to secrets, configs, or env vars.
    """
    handler = DworshakObtain()
    if store == StoreMode.CONFIG:
        return handler.config(service=service_or_key, item=item, message=message, default=default, **kwargs)
    elif store == StoreMode.SECRET:
        return handler.secret(service=service_or_key, item=item, message=message, default=default, **kwargs)
    elif store == StoreMode.ENV:
        # Note: for ENV, service_or_key is the actual key
        return handler.env(key=service_or_key, message=message, default=default, **kwargs)
    
    raise ValueError(f"Unsupported StoreMode: {store}")
