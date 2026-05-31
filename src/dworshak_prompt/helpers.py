# src/dworshak_prompt/helpers.py
from __future__ import annotations
import re
from typing import List, Set
from enum import Enum
import logging
logger=logging.getLogger(__name__) # debug handled by CLI flag, --debug

class PromptMode(Enum):
    CONSOLE = "console"
    GUI = "gui"
    WEB = "web"

class InterruptBehavior(Enum):
    EXIT = "exit"
    RETURN_DEFAULT = "use_default"
    RETURN_NONE = "return_none"
    RAISE = "raise"

def resolve_str_to_set(instance: str | Set[PromptMode] | None) -> Set[PromptMode]:
    if not instance:
        return set()
    if isinstance(instance, set):
        return instance
    if isinstance(instance, str):
        # Split on commas, spaces, or +; filter empties
        items = re.split(r'[,\s+]+', instance)
        items = [i.strip() for i in items if i.strip()]
        try:
            return {PromptMode[item.upper()] for item in items}  # Enum keys are uppercase, e.g., "console" -> CONSOLE
        except KeyError as e:
            raise ValueError(f"Invalid PromptMode: {e}")
    raise ValueError(f"Invalid type for set: {type(instance)}")

def resolve_str_to_list(instance: str | List[PromptMode] | None) -> List[PromptMode]:
    if not instance:
        return []
    if isinstance(instance, list):
        return instance
    if isinstance(instance, str):
        # Split on commas, spaces, or +; filter empties
        items = re.split(r'[,\s+]+', instance)
        items = [i.strip() for i in items if i.strip()]
        try:
            return [PromptMode[item.upper()] for item in items]
        except KeyError as e:
            raise ValueError(f"Invalid PromptMode: {e}")
    raise ValueError(f"Invalid type for list: {type(instance)}")

def init_x11_threads():
    """Ensures X11 is initialized in thread-safe mode before any UI call."""
    import sys
    if sys.platform.startswith('linux'):
        import ctypes
        # Use find_library to ensure we get the right path
        from ctypes.util import find_library

    if sys.platform.startswith('linux'):
        try:
            lib_path = find_library('X11')
            if lib_path:
                x11 = ctypes.cdll.LoadLibrary(lib_path)
                # Attempt to initialize thread safety
                status = x11.XInitThreads()
                if status:
                    logger.debug(f"XInitThreads() succeeded (status: {status})")
                else:
                    logger.warning("XInitThreads() returned 0; might be too late.")
            else:
                logger.error("Could not locate X11 library.")
        except Exception as e:
            logger.debug(f"Failed to init X threads: {e}")
