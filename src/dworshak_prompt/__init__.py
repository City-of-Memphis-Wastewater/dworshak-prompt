__all__ = [
    "DworshakPrompt", 
    "dworshak_ask",
    "PromptMode",
    "Obtain",
    "dworshak_obtain",
    "StoreMode"
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
    
    if name == "dworshak_obtain":
        from .obtain import dworshak_obtain
        return dworshak_obtain
    
    if name == "StoreMode":
        from .obtain import StoreMode
        return StoreMode
    

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(__all__ + [
        "__all__", "__builtins__", "__cached__", "__doc__", "__file__",
        "__getattr__", "__loader__", "__name__", "__package__", "__path__", "__spec__"
    ])
