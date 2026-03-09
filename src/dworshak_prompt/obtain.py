# src/dworshak_prompt/obtain.py
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any
import sys

from dworshak_config import DworshakConfig
from dworshak_env import DworshakEnv
from .multiplexer import DworshakPrompt

"""
The obtain pattern.
"""

'''
class StoreMode(Enum):
    CONFIG = "config"
    SECRET = "secret"
    ENV = "env"
'''
@dataclass
class ObtainResult:
    value: Optional[str] = None
    is_new: Optional[bool] = False  # True=New, False=Known, None=Cancelled

    @property
    def status_message(self) -> str:
        """Generic statuses that work for any key/service."""
        return {
            True: "Value stored.",
            False: "Value resolved.",
            None: "Exited."
        }.get(self.is_new, "Error.")

    def __bool__(self):
        return self.value is not None

@dataclass
class SecretData(ObtainResult):
    """Overrides status for secret-specific phrasing."""
    @property
    def status_message(self) -> str:
        return {
            True: "Secret stored.",
            False: "Secret known.",
            None: "Exited."
        }.get(self.is_new, "Error.")

    def __repr__(self):
        return f"SecretData(is_new={self.is_new}, value='********')"

# Alias for clarity, or specialized if Config needs different status phrasing
ConfigData = ObtainResult
EnvData = ObtainResult

class Obtain:
    def __init__(self,
        config_path: str | Path | None = None,
        secret_path: str | Path | None = None,
        env_path: str | Path | None = None,
    ):
        self.config_path = config_path
        self.secret_path = secret_path
        self.env_path = env_path

    def ask(self, *args, **kwargs):
        """
        Proxy to the multiplexer for direct questions.
        I don't this we need this, it is bad hygiene.
        """
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
        priority_interface: str | None = None,
        avoid_interface: str | None = None,
        path: str | Path | None = None,
        overwrite: bool = False,
        forget: bool = False,
        **kwargs # Pass-through for priority_interface, avoid_interface, debug, etc.
    ) -> ConfigData:
        if path is None:
            path = self.config_path
            
        config_mgr = DworshakConfig(path = path)
        value = config_mgr.get(service, item)

        # Logic: If it exists and we aren't forcing a refresh, return it.
        if value is not None and not overwrite:
            return ConfigData(value=value, is_new=False)

        # If missing or overwriting, we use the multiplexer
        new_value = DworshakPrompt().ask(
            message=message or f"Please input CONFIG value\n(service = {service}, item = {item})",
            suggestion=suggestion or value,
            priority_interface = priority_interface,
            avoid_interface = avoid_interface, 
            hide_input=False,
            **kwargs # Pass-through for priority_interface, avoid_interface, debug, etc.
        )

        # Persistence logic
        if new_value is None:
            return ConfigData(value=None, is_new=None)
            
        if not forget:
            config_mgr.set(service, item, new_value, overwrite=overwrite)
            
        return ConfigData(value=new_value, is_new=True)

    def secret(
        self,
        service: str, 
        item: str, 
        message: str | None = None,
        suggestion: str | None = None,
        default: Any | None = None,
        priority_interface: str | None = None,
        avoid_interface: str | None = None,
        path: str | Path | None = None,
        overwrite: bool = False,
        forget: bool = False,
        **kwargs 
        )-> SecretData:

        if path is None:
            path = self.secret_path
        #import cryptography
        #from dworshak_secret import DworshakSecret, get_secret, store_secret
        try:
            # Lazy Import dworshak_secret here to mitigate top-level crashes
            import cryptography
            from dworshak_secret import DworshakSecret, get_secret, store_secret
        except:
            # Trigger the "Lifeboat" redirection error
            from memphisdrip import safe_notify
            from .messages import notify_missing_function_redirect, MSG_CRYPTO_EXTRA
            # We pass a specific context so the user knows why it failed
            full_msg = notify_missing_function_redirect("Obtain.secret()") + MSG_CRYPTO_EXTRA
            safe_notify(full_msg)
            raise SystemExit(1)
        
        # Similar logic for secrets, but using dworshak-secret
        value = get_secret(service, item)
        if value is not None and not overwrite:
            return SecretData(value = value, is_new = False)
        
        new_value = DworshakPrompt().ask(
            message=message or f"Please input SECRET value\n(service = {service}, item = {item})",
            hide_input=True,
            priority_interface = priority_interface,
            avoid_interface = avoid_interface, 
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
        priority_interface: str | None = None,
        avoid_interface: str | None = None,
        path: str | Path | None = None,
        overwrite: bool = False,
        forget: bool = False,
        **kwargs
    ) -> EnvData:
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
            return EnvData(value=value, is_new=False)

        # If missing or overwriting, we use the multiplexer
        new_value = DworshakPrompt().ask(
            message=message or f"Please input ENV value\n(key = {key})",
            suggestion=value or default,
            priority_interface = priority_interface,
            avoid_interface = avoid_interface, 
            hide_input=False,
            **kwargs
        )

        # Persistence logic: Save to .env file if not forgotten
        if new_value is None:
            return EnvData(value=None, is_new=None)

        if not forget:
            env_mgr.set(key, new_value, overwrite=overwrite)

        return EnvData(value=new_value, is_new=True)
'''
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
    handler = Obtain()
    if store == StoreMode.CONFIG:
        return handler.config(service=service_or_key, item=item, message=message, default=default, **kwargs)
    elif store == StoreMode.SECRET:
        return handler.secret(service=service_or_key, item=item, message=message, default=default, **kwargs)
    elif store == StoreMode.ENV:
        # Note: for ENV, service_or_key is the actual key
        return handler.env(key=service_or_key, message=message, default=default, **kwargs)
    
    raise ValueError(f"Unsupported StoreMode: {store}")
'''
