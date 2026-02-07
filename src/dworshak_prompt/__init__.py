"""
from .multiplexer import DworshakPrompt

all = [
    "DworshakPrompt"
]
"""

__all__ = ["DworshakPrompt"]

def __getattr__(name):
    if name == "DworshakPrompt":
        from .multiplexer import DworshakPrompt
        return DworshakPrompt
    raise AttributeError(name)
