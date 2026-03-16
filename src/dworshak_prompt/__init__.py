# src/*/__init__.py
from __future__ import annotations

__all__ = [
    "DworshakPrompt", 
    "dworshak_ask",
    "PromptMode",
    "Obtain",
    "obtain",
    "InterruptBehavior"
    ]

def __getattr__(name):
    if name == "DworshakPrompt":
        from .multiplexer import DworshakPrompt
        return DworshakPrompt
    
    if name == "dworshak_ask":
        from .multiplexer import dworshak_ask
        return dworshak_ask
    
    if name == "PromptMode":
        from .helpers import PromptMode
        return PromptMode

    if name == "Obtain":
        from .obtain import Obtain
        return Obtain

    if name == "obtain":
        from .obtain import obtain
        return obtain

    if name == "InterruptBehavior":
        from .helpers import InterruptBehavior
        return InterruptBehavior

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(__all__ + [
        "__all__", "__builtins__", "__cached__", "__doc__", "__file__",
        "__getattr__", "__loader__", "__name__", "__package__", "__path__", "__spec__"
    ])
