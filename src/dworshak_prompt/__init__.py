__all__ = [
    "DworshakPrompt", 
    "PromptMode"
    ]

def __getattr__(name):
    if name == "DworshakPrompt":
        from .multiplexer import DworshakPrompt
        return DworshakPrompt
    
    if name == "PromptMode":
        from .multiplexer import PromptMode
        return PromptMode
        
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
