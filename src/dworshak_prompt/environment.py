# src/dworshak_prompt/environment.py
"""
Typer-based console prompt. Non ideal for tty.
"""
from __future__ import annotations
import os
import sys
    
def has_real_tty() -> bool:
    # Check if we can reach the user via /dev/tty (the sideband)
    if os.path.exists("/dev/tty"):
        return True
    
    # Fallback for Windows or systems where stderr is still a TTY
    try:
        if sys.stderr.isatty():
            return True
    except Exception:
        pass
        
    return False
"""
def has_real_tty():
    # Check standard streams first
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            if os.isatty(stream.fileno()):
                return True
        except Exception:
            continue
    # If standard streams are redirected, check the device itself
    return os.path.exists("/dev/tty")
"""
def get_console_provider():
    # 1. If we are in a normal interactive terminal, use the 'pretty' version
    if sys.stdin.isatty():
        try:
            from .console_prompt import console_get_input
            return console_get_input
        except ImportError:
            pass

    # 2. If stdin is NOT a TTY (like VAR=$(...)), try the Sideband TTY
    if os.path.exists("/dev/tty"):
        from .console_prompt_tty import console_get_input_tty_prompt
        return console_get_input_tty_prompt

    # 3. Absolute fallback (Windows or CI)
    from .console_prompt_stdlib import console_get_input_stdlib
    return console_get_input_stdlib

def is_likely_ci_or_non_interactive() -> bool:
    """
    Heuristic to determine if we should skip interactive prompting.
    In Dworshak, we only return True if there is NO path to the user.
    """
    # 1. If /dev/tty exists, we HAVE a path to the user, regardless of CI env vars.
    if os.path.exists("/dev/tty"):
        return False

    # 2. If we are on Windows and stdin is a TTY, we are interactive.
    if os.name == "nt" and sys.stdin.isatty():
        return False

    # 3. Check common CI fingerprints
    ci_markers = [
        "GITHUB_ACTIONS", "GITLAB_CI", "CIRCLECI", "TRAVIS", 
        "JENKINS_URL", "TF_BUILD", "CI", "BUILD_ID"
    ]
    for var in ci_markers:
        val = os.getenv(var)
        if val and val.lower() not in ("", "false", "0", "no"):
            return True

    # 4. Container detection
    if os.path.exists("/.dockerenv"):
        return True

    # 5. Fallback: If stdin is not a TTY and no /dev/tty exists, we are non-interactive.
    return not sys.stdin.isatty()