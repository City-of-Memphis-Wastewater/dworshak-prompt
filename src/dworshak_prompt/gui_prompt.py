# src/dworshak_prompt/gui_prompt.py
from __future__ import annotations
# tkinter workaround for wsl2, first, before other imports
import logging
logger=logging.getLogger(__name__)
import sys
if sys.platform.startswith('linux'):
    try:
        import ctypes
        # Use find_library to ensure we get the right path
        from ctypes.util import find_library
        lib_path = find_library('X11')
        if lib_path:
            x11 = ctypes.cdll.LoadLibrary(lib_path)
            x11.XInitThreads()
            logger.debug("XInitThreads() invoked.")
    except Exception as e:
        logger.debug(f"Failed to init X threads: {e}")
try:
    import tkinter as tk
except ImportError:
    pass
from typing import Optional
import platform
import sys
import pyhabitat

class CustomPromptDialog:
    def __init__(self, parent, title, message, suggestion="", hide_input=False):
        self.result = None
        self.hide_input = hide_input
        
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        #self.top.attributes("-topmost", True)
        self.top.resizable(False, False)
        
        
        # Set a minimum width and padding
        # We target ~400px width to ensure the title isn't truncated
        min_w, min_h = 400, 150
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
        #self.top.grab_set()  # Make it modal
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

def gui_get_input(message: str, suggestion: str | None = None, hide_input: bool = False) -> Optional[str]:
    """
    Displays a custom modal GUI popup with an optional Show/Hide toggle.
    """
    try:
        root = tk.Tk()
        #root.withdraw()
        root.title("dworshak-prompt")
        # Use our custom dialog instead of simpledialog
        dialog = CustomPromptDialog(root, "dworshak-prompt", message, suggestion, hide_input)
        
        return dialog.result

    finally:
        root.destroy()



def get_tkinter_hint() -> str:
    os_name = platform.system().lower()
    hint_base = (
        "GUI mode skipped: Tkinter unavailable.\n"
        "Tkinter is Python's standard GUI library, but it may need installation or configuration.\n"
        "Common fixes:\n"
    )

    if "darwin" in os_name:  # macOS
        return hint_base + (
            "• On macOS: Install via Homebrew (brew install python-tk) or your Python installer (e.g., python.org download with Tkinter option).\n"
            "• Ensure your Python is built with Tcl/Tk support: python -m tkinter (should open a window).\n"
            "More: https://docs.python.org/3/library/tkinter.html#installing-tk"
        )

    elif "linux" in os_name:
        if pyhabitat.on_termux():
            return hint_base + (
                "• In Termux: Install python-tkinter (pkg install python-tkinter ).\n"
                "• For GUI support, set up X11 forwarding (https://wiki.termux.com/wiki/Graphical_Environment).\n"
                "More: https://wiki.termux.com/wiki/Python"
            )
        elif pyhabitat.on_wsl():  # WSL-specific
            return hint_base + (
                "• In WSL: Install python3-tk (sudo apt install python3-tk for Ubuntu/Debian).\n"
                "• For GUI support, enable WSLg (Windows 11+ WSL) or set up X11 forwarding (e.g., Xming or VcXsrv on Windows).\n"
                "• Test: python3 -m tkinter (should open a window).\n"
                "More: https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps"
            )
        else:  # General Linux
            return hint_base + (
                "• On Linux: Install via your package manager (e.g., sudo apt install python3-tk on Ubuntu/Debian, or sudo dnf install python3-tkinter on Fedora).\n"
                "• Test: python3 -m tkinter (should open a window).\n"
                "More: https://docs.python.org/3/library/tkinter.html#installing-tk"
            )

    elif "windows" in os_name:
        return hint_base + (
            "• On Windows: Tkinter is usually bundled with Python installers from python.org (check 'tcl/tk and IDLE' option).\n"
            "• If missing, reinstall Python with the option enabled.\n"
            "• Test: python -m tkinter (should open a window).\n"
            "More: https://docs.python.org/3/library/tkinter.html#installing-tk"
        )

    else:  # Generic fallback
        return hint_base + (
            "• Install Tkinter via your Python distribution or package manager.\n"
            "• Test: python -m tkinter (should open a window).\n"
            "More: https://docs.python.org/3/library/tkinter.html#installing-tk"
        )
