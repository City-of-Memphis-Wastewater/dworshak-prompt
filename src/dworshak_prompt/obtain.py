# src/dworshak_prompt/obtain.py
from __future__ import annotations
from typing import Literal, Optional
from dataclasses import dataclass
from dworshak_config import DworshakObtain


@dataclass
class SecretData:
    value: Optional[str]
    is_new: Optional[bool] = False

    def __repr__(self):
        return "SecretData(value='********', is_new=%s)" % self.is_new

    def __bool__(self):
        return self.value is not None


def obtain(
    *,
    prompt,
    service: str,
    item: str,
    store: Literal["config", "secret"] = "config",
    overwrite: bool = False,
    forget: bool = False,
    suggestion: Optional[str] = None,
    default: Optional[str] = None,
    prompt_message: Optional[str] = None,
    hide_input: Optional[bool] = None,
    **prompt_kwargs,
):
    """
    Obtain a value from storage, a human, or a safe default.

    This function defines the core human-first configuration contract.
    """

    # ---------- CONFIG ----------
    if store == "config":
        mgr = DworshakObtain(path=prompt.config_path)
        value = mgr.get(service, item)

        if value is not None and not overwrite:
            return value

        if prompt.is_interactive:
            new_value = prompt.ask(
                message=prompt_message or f"{service} / {item}",
                suggestion=suggestion or value,
                hide_input=hide_input or False,
                **prompt_kwargs,
            )
            if new_value is not None:
                if not forget:
                    mgr.set(service, item, new_value)
                return new_value

        # Non-interactive or cancelled
        return default if default is not None else value

    # ---------- SECRET ----------
    if store == "secret":
        try:
            from dworshak_secret import get_secret, store_secret
        except Exception:
            from memphisdrip import safe_notify
            from .messages import notify_missing_function_redirect, MSG_CRYPTO_EXTRA

            safe_notify(
                notify_missing_function_redirect("obtain(store='secret')")
                + MSG_CRYPTO_EXTRA
            )
            raise SystemExit(1)

        value = get_secret(service, item)

        if value is not None and not overwrite:
            return SecretData(value=value, is_new=False)

        if prompt.is_interactive:
            new_value = prompt.ask(
                message=prompt_message or f"{service} / {item}",
                hide_input=True if hide_input is None else hide_input,
                **prompt_kwargs,
            )
            if new_value is not None:
                if not forget:
                    store_secret(service, item, new_value)
                return SecretData(value=new_value, is_new=True)

        # Non-interactive fallback
        if default is not None:
            return SecretData(value=default, is_new=None)

        return SecretData(value=None, is_new=None)

    raise ValueError(f"Unknown store type: {store}")
