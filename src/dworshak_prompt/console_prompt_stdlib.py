# src/dworshak_prompt/console_prompt_stdlib.py
import sys
import getpass
from .keyboard_interrupt import PromptCancelled

import logging
logger = logging.getLogger(__name__)

def console_get_input_stdlib(
    message: str, 
    suggestion: str | None = None, 
    hide_input: bool = False
) -> str:
    """
    A pure standard-library fallback for user input.
    Ensures zero dependencies while maintaining a professional CLI feel.
    If a suggestion is provided while hide is True, the suggestion is ignored.
    """
    
    # Construct the prompt string
    # e.g., "Enter username [admin]: "
    prompt_str = message
    if suggestion and not hide_input:
        prompt_str = f"{message} [{suggestion}]"
    
    prompt_str = f"{prompt_str}: ".replace("::", ":") # Cleanup double colons

    try:
        if hide_input:
            sgst_msg=""
            if suggestion:
                logger.debug("Credential suggestion not shown in console for security. Please use PromptMode.WEB or PromptMode.GUI to enjoy suggestion autofill for credentials.", file = sys.stderr)
                sgst_msg=" (suggestion hidden)"
            # getpass handles terminal echoing automatically
            hidden_prompt = f"{message} (input hidden){sgst_msg}: "
            response = getpass.getpass(hidden_prompt)
                
        else:
            # Standard logic for visible input
            if suggestion:
                prompt_str = f"{message} [{suggestion}]: ".replace("::", ":")
            response = input(prompt_str)

        # Handle the 'Enter' key with a suggestion
        if not response and suggestion:
            return suggestion
            
        return response

    except (KeyboardInterrupt, EOFError):
        # We catch Ctrl+C (KeyboardInterrupt) or Ctrl+D (EOFError)
        # We print a newline so the shell prompt doesn't end up on the same line
        sys.stdout.write("\n")
        sys.stdout.flush()
        raise PromptCancelled()