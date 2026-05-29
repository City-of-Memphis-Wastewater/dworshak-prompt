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
    tk=None
from typing import Optional
import platform
import sys
import pyhabitat

class CustomPromptDialog:
    def __init__(self, root, title, message, suggestion="", hide_input=False):
        self.result = None
        self.hide_input = hide_input
        
        self.root = root
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.lift()
        
        # Set a minimum width and padding
        # We target ~400px width to ensure the title isn't truncated
        min_w, min_h = 400, 150
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        # Center with the new dimensions
        x = (screen_w // 2) - (min_w // 2)
        y = (screen_h // 2) - (min_h // 2)
        self.root.geometry(f"{min_w}x{min_h}+{x}+{y}")
        self.root.minsize(min_w, min_h)

        tk.Label(self.root, text=message, wraplength=300, justify="left", padx=10, pady=10).pack(fill ="x")

        # Input container
        entry_frame = tk.Frame(self.root, padx=10)
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
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()
        tk.Button(btn_frame, text="OK", command=self.on_ok, width=10).pack(side="left", padx=5)
        #tk.Button(btn_frame, text="Submit Empty String", command=self.on_submit_empty_string, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.on_cancel, width=10).pack(side="left", padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_cancel)
        #self.root.grab_set()  # Make it modal
        #parent.wait_window(self.root)
        self.root.update_idletasks()
        self.root.lift()

        if not pyhabitat.on_wsl():
            if True:
            #try:
                self.root.attributes("-topmost",True)
                self.root.after(
                    200,
                    lambda: self.root.attributes("-topmost",False),
                )
            #except Exception as e:
            #    pass
        self.entry.focus_force()

    def toggle_visibility(self):
        if self.entry.cget("show") == "*":
            self.entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.entry.config(show="*")
            self.toggle_btn.config(text="Show")

    def on_ok(self):
        self.result = self.entry.get()
        self.root.destroy()

    #def on_submit_empty_string(self):
    #    self.result = ""
    #    self.root.destroy()

    def on_cancel(self):
        self.root.destroy()

def gui_get_input(message: str, suggestion: str | None = None, hide_input: bool = False) -> Optional[str]:
    """
    Displays a custom modal GUI popup with an optional Show/Hide toggle.
    """
    if tk is None:
        return None
    root = tk.Tk()

    if True:
    #try:
        # Use custom dialog instead of simpledialog
        dialog = CustomPromptDialog(
            root=root, 
            title="dworshak-prompt", 
            message=message, 
            suggestion=suggestion or "", 
            hide_input=hide_input)

        root.mainloop()
        
        return dialog.result
    #if True:
    #finally:
    #    try:
    #        root.destroy()
    #    except Exception as e:
    #        pass


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
