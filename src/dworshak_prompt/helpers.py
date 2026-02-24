# src/dworshak_prompt/helpers.py
from __future__ import annotations
import re
from typing import List
from enum import Enum

class PromptMode(Enum):
    CONSOLE = "console"
    GUI = "gui"
    WEB = "web"

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