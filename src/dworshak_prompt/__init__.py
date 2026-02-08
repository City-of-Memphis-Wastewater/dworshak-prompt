__all__ = [
    "DworshakPrompt", 
    "PromptMode"
    ]

def __getattr__(name):
    if name == "DworshakPrompt":
        from .multiplexer import DworshakPrompt
        return DworshakPrompt
    raise AttributeError(name)

def __getattr__(name):
    if name == "PromptMode":
        from .multiplexer import PromptMode
        return PromptMode
    raise AttributeError(name)
