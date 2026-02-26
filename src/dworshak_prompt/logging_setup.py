# src/dworshak_prompt/logging_setup.py
from __future__ import annotations
import logging
import sys

# --- Existing code copied from multiplexer.py, 2/26/2026 ---

# Setup logger
logger = logging.getLogger("dworshak_prompt")
# Default to INFO to hide diagnostics; change to DEBUG to see them
#logger.setLevel(logging.INFO) 
logger.setLevel(logging.WARNING) 
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(_handler)

# --- Hypothetical new logger setup code, 2/26/2026 ---

def setup_logging(level=logging.WARNING):
    logger = logging.getLogger("dworshak_prompt")
    logger.setLevel(level)

    # Remove any existing handlers to avoid duplicates
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Optional: file handler for more detail
    # file_handler = logging.FileHandler("dworshak.log")
    # file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger

"""
# in cli.py (and similarly in cli_stdlin.py)

# src/dworshak_prompt/cli.py (top of file)
from .logging_config import setup_logging

# At the very top, before any other imports that use logger
setup_logging(level=logging.WARNING)  # or DEBUG if --debug/--verbose

....

verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed operation messages.")
debug: bool = typer.Option(False, "--debug", help="Show low-level diagnostics and tracebacks.")

# Then pass to ask / obtain functions
val = DworshakPrompt().ask(..., verbose=verbose, debug=debug)

# And in ask() / obtain():
if debug:
    setup_logging(logging.DEBUG)
elif verbose:
    setup_logging(logging.INFO)
else:
    setup_logging(logging.WARNING)

"""


"""
# Any file (server.py, web_prompt.py, multiplexer.py, etc.)
import logging

logger = logging.getLogger("dworshak_prompt")  # ← same name everywhere

# Then use:
logger.debug("Polling started")
logger.info("Server running on port %d", port)
logger.warning("Missing req_id in cancel request")
logger.error("Unexpected exception", exc_info=True)
"""