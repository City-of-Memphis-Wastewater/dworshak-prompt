# src/dworshak_prompt/gui_prompt.py
from __future__ import annotations # Delays annotation evaluation, allowing modern 3.10+ type syntax and forward references in older Python versions 3.8 and 3.9
import tkinter as tk
from tkinter import simpledialog
from typing import Optional


def gui_get_input(prompt_message: str, hide_input: bool = False) -> Optional[str]:
    """
    Displays a modal GUI popup to get input.
    Improved for WSLg stability.
    """
    root = None
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Lift the window to the top so it doesn't hide behind the terminal
        root.attributes("-topmost", True)

        show_char = '*' if hide_input else ''

        # askstring handles its own internal event loop
        value = simpledialog.askstring(
            title="Config Input",
            prompt=prompt_message,
            show=show_char
        )
        
        return value
        
    except Exception as e:
        # Avoid dumping the whole XML/Trace, but log the error type
        print(f"GUI Error: {type(e).__name__}")
        return None
    finally:
        if root:
            # Proper cleanup for X11/WSLg
            root.quit() # Stop the event loop
            root.destroy()