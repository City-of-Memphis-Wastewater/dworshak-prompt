# src/dworshak_prompt/logging_setup.py
import logging
import sys
import traceback

def setup_logging(verbose: bool = False, debug: bool = False, initial: bool=False):
    """
    Configure the root 'dworshak_prompt' logger.
    Priority: debug > verbose > default (WARNING)
    """
    logger = logging.getLogger("dworshak_prompt")

    # Clear any existing handlers to prevent duplicates
    logger.handlers.clear()

    # Choose level
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)

    # Simple, clean format (no timestamps unless debug)
    if debug:
        formatter = logging.Formatter('%(levelname)s [%(name)s] %(message)s  (%(filename)s:%(lineno)d)')
    else:
        formatter = logging.Formatter('%(message)s')

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional: file logging (uncomment if you want persistent logs)
    # file_handler = logging.FileHandler("dworshak.log")
    # file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s'))
    # logger.addHandler(file_handler)
    if initial:
        logger.debug("Logging initialized at level %s", logging.getLevelName(level))
    return logger


def log_traceback(logger):
    if logger.level <= logging.DEBUG:
        traceback.print_exc(file=sys.stderr)
