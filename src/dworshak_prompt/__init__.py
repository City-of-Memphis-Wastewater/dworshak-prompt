__all__ = [
    "DworshakPrompt", 
    "PromptMode"
    "DworshakObtain"
    ]

def __getattr__(name):
    if name == "DworshakPrompt":
        from .multiplexer import DworshakPrompt
        return DworshakPrompt
    
    if name == "PromptMode":
        from .multiplexer import PromptMode
        return PromptMode

    if name == "DworshakObtain":
        from .get import DworshakObtain
        return DworshakObtain

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(__all__ + [
        "__all__", "__builtins__", "__cached__", "__doc__", "__file__",
        "__getattr__", "__loader__", "__name__", "__package__", "__path__", "__spec__"
    ])
