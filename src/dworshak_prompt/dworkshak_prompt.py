# src/dworshak_prompt/dworshak_prompt.py
from __future__ annotations
from .multiplexer import ask as _ask
from .obtain import obtain as _obtain

class DworshakPrompt:
    ask = staticmethod(_ask)
    obtain = staticmethod(_obtain)
