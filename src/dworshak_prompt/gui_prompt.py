# src/dworshak_prompt/gui_prompt.py
from __future__ import annotations # Delays annotation evaluation, allowing modern 3.10+ type syntax and forward references in older Python versions 3.8 and 3.9
import tkinter as tk
from tkinter import simpledialog
from typing import Optional


def gui_get_input(prompt_message: str,  suggestion: str | None = None,  hide_input: bool = False) -> Optional[str]:
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

        # Customizing the dialog to handle defaults
        if hide_input:
            # Simpledialog doesn't support 'show="*"' natively in the basic call
            # For a true production GUI, you'd use a Toplevel with an Entry(show="*")
            val = simpledialog.askstring("Input", message, show='*')
        else:
            # 'initialvalue' is the key for suggested values in tkinter
            val = simpledialog.askstring("Input", message, initialvalue=suggestion or "")
        
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