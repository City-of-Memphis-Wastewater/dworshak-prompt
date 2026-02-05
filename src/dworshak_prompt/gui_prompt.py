# src/dworshak_prompt/gui_prompt.py
from __future__ import annotations
import tkinter as tk
from tkinter import simpledialog
from typing import Optional

def gui_get_input(prompt_message: str, suggestion: str | None = None, hide_input: bool = False) -> Optional[str]:
    """
    Displays a modal GUI popup to get input.
    """
    root = tk.Tk()
    root.withdraw()
    
    # Lift the window to the top
    root.attributes("-topmost", True)

    try:
        if hide_input:
            # simpledialog uses 'show' for password masking
            val = simpledialog.askstring("Input Required", prompt_message, show='*')
        else:
            val = simpledialog.askstring("Input Required", prompt_message, initialvalue=suggestion or "")
        
        # val will be None if the user clicks 'Cancel' or the 'X'
        return val
        
    finally:
        # Proper cleanup for X11/WSLg/Windows
        root.destroy()