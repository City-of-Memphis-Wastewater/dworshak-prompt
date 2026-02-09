# src/dworshak_prompt/gui_prompt.py
from __future__ import annotations
try:
    import tkinter as tk
except ImportError:
    pass
from typing import Optional

class CustomPromptDialog:
    def __init__(self, parent, title, message, suggestion="", hide_input=False):
        self.result = None
        self.hide_input = hide_input
        
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.attributes("-topmost", True)
        self.top.resizable(False, False)
        
        
        # Set a minimum width and padding
        # We target ~400px width to ensure the title isn't truncated
        min_w, min_h = 400, 180
        screen_w = parent.winfo_screenwidth()
        screen_h = parent.winfo_screenheight()
        
        # Center with the new dimensions
        x = (screen_w // 2) - (min_w // 2)
        y = (screen_h // 2) - (min_h // 2)
        self.top.geometry(f"{min_w}x{min_h}+{x}+{y}")
        self.top.minsize(min_w, min_h)

        tk.Label(self.top, text=message, wraplength=300, justify="left", padx=10, pady=10).pack(fill ="x")

        # Input container
        entry_frame = tk.Frame(self.top, padx=10)
        entry_frame.pack(fill="x")

        self.entry = tk.Entry(entry_frame, font=("sans-serif", 10))
        if hide_input:
            self.entry.config(show="*")
        self.entry.insert(0, suggestion or "")
        self.entry.pack(side="left", expand=True, fill="x")
        self.entry.bind("<Return>", lambda e: self.on_ok())
        self.entry.focus_set()

        # Toggle Button (Only if hide_input is True)
        if hide_input:
            self.toggle_btn = tk.Button(entry_frame, text="Show", command=self.toggle_visibility, width=5)
            self.toggle_btn.pack(side="right", padx=(5, 0))

        # Action Buttons
        btn_frame = tk.Frame(self.top, pady=10)
        btn_frame.pack()
        tk.Button(btn_frame, text="OK", command=self.on_ok, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.on_cancel, width=10).pack(side="left", padx=5)

        self.top.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.top.grab_set()  # Make it modal
        parent.wait_window(self.top)

    def toggle_visibility(self):
        if self.entry.cget("show") == "*":
            self.entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.entry.config(show="*")
            self.toggle_btn.config(text="Show")

    def on_ok(self):
        self.result = self.entry.get()
        self.top.destroy()

    def on_cancel(self):
        self.top.destroy()

def gui_get_input(prompt_message: str, suggestion: str | None = None, hide_input: bool = False) -> Optional[str]:
    """
    Displays a custom modal GUI popup with an optional Show/Hide toggle.
    """
    try:
        root = tk.Tk()
        root.withdraw()

        # Use our custom dialog instead of simpledialog
        dialog = CustomPromptDialog(root, "dworshak-prompt", prompt_message, suggestion, hide_input)
        
        return dialog.result

    finally:
        root.destroy()