# src/dworshak_prompt/dworshak_prompt.py
from __future__ annotations
from .multiplexer import ask as _ask
from .obtain import obtain as _obtain

class DworshakPrompt:
    def __init__(
        self,
        *,
        config_path: str | None = None,
        secret_path: str | None = None,
        default_priority=None,
        default_avoid=None,
    ):
        self.config_path = config_path
        self.secret_path = secret_path
        self.default_priority = default_priority
        self.default_avoid = default_avoid

    def ask(self, *args, **kwargs):
        return _ask(
            *args,
            priority=kwargs.get("priority", self.default_priority),
            avoid=kwargs.get("avoid", self.default_avoid),
            **kwargs,
        )

    def obtain(
        self,
        *,
        service: str,
        item: str,
        store: str = "config",
        overwrite: bool = False,
        forget: bool = False,
        **prompt_kwargs,
    ) -> str | None:
        return _obtain(
            prompt=self,
            config_path=self.config_path,
            secret_path=self.secret_path,
            service=service,
            item=item,
            store=store,
            overwrite=overwrite,
            forget=forget,
            **prompt_kwargs,
        )
