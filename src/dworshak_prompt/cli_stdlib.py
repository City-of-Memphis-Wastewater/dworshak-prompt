# src/dworshak_prompt/cli_stdlib.py
from __future__ import annotations
from .logging_setup import setup_logging
# Initialize logging before anything else
logger=setup_logging(verbose=False, debug=False, initial=True)  # Default off
import argparse
import sys
from memphisdrip import safe_notify

from . import DworshakPrompt, PromptMode
from .keyboard_interrupt import PromptCancelled
from ._version import __version__

from .messages import (
    MSG_CRYPTO_EXTRA, 
    MSG_FULL_EXTRA,
    stdlib_notify_missing_command_redirect
)

def run_prompt(
    message: str = "Enter value",
    suggestion: str | None = None,
    hide_input: bool = False,
    debug: bool = False,
    verbose: bool = False,
    priority_interface: list[PromptMode] | None = None,
    avoid_interface: list[PromptMode] | None = None,
) -> int:

    setup_logging(verbose=verbose, debug=debug)

    priority_interface_list = priority_interface if priority_interface is not None else None
    avoid_interface_set = set(avoid_interface) if avoid_interface is not None else None
    

    try:
        value = DworshakPrompt().ask(
            message=message,
            suggestion=suggestion,
            hide_input=hide_input,
            priority_interface=priority_interface_list,
            avoid_interface = avoid_interface_set,
            debug=debug,
            verbose=verbose,
        )
        if value is not None:
            safe_notify(value)
            return 0
        else:
            safe_notify("Input cancelled or no method succeeded.")
            return 1

    except PromptCancelled:
        safe_notify("Prompt cancelled by user.")
        return 130
    except KeyboardInterrupt:
        safe_notify("Interrupted.")
        return 130
    except Exception as e:
        safe_notify(f"Error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return 1


def stdlib_notify_redirect(command: str):
    """
    Detailed notification for Typer-only commands with platform-specific guidance.
    """
    msg_missing_typer_command = stdlib_notify_missing_command_redirect(command)
    msg = msg_missing_typer_command + MSG_CRYPTO_EXTRA + MSG_FULL_EXTRA
    safe_notify(msg)
    

def main():
    # --- Typer-Only Commands ---
    # Pre-check sys.argv for Typer-only commands (fast, no parsing)
    argv_lower = [arg.lower() for arg in sys.argv[1:]]
    typer_only = {"obtain", "helptree"}

    for cmd in typer_only:
        if cmd in argv_lower:
            stdlib_notify_redirect(cmd)
            return 1

    parser = argparse.ArgumentParser(
        prog="dworshak-prompt",
        description=f"Multiplexed user input via console, GUI, and web. (v{__version__})",
        add_help=False,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=False,
        title="Commands",          # Overrides "positional arguments"
        help="Available commands",
    )

    # ask subcommand – exact match in name, help text, flags
    ask_parser = subparsers.add_parser(
        "ask",
        help="Get user input and print it to stdout",
        description="Prompt the user using available methods.",
        add_help=False,
    )

    # Change from --message to a positional argument
    ask_parser.add_argument(
        "message",
        nargs="?",                # Makes it optional
        #default="Enter value",
        default=None,
        help="The prompt message to display",
    )

    ask_parser.add_argument(
        "--message",
        "-M",
        #default="Enter value",
        default=None,
        dest="message_flag",      # Store it separately to mitigate conflict
        help="The prompt message to display (overwrites positional argument)",
    )
    ask_parser.add_argument(
        "--suggestion",
        "-s",
        default=None,
        help="Suggested/default value",
    )
    ask_parser.add_argument(
        "--hide",
        "-H",
        action="store_true",
        help="Hide input (password mode)",
    )
    ask_parser.add_argument(
        "--interface", "-i", 
        choices=[m.value for m in PromptMode], 
        default=None,#PromptMode.CONSOLE.value,
        type=str.lower,
        help="Preferred input mode (case-insensitive)",
    )
    ask_parser.add_argument(
        "--avoid", "-a", 
        choices=[m.value for m in PromptMode], 
        default=None,
        type=str.lower,
        help="Avoided input mode (case-insensitive)",
    )
    ask_parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug logging",
    )
    ask_parser.add_argument(
        "--verbose","-v",
        action="store_true",
        help="Enable verbose logging",
    )

    # Help flags at both levels
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit",
    )
    ask_parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if args.command == "ask":
        interface_mode_map = {m.value: m for m in PromptMode}

        # Convert repeated --interface to ordered list of PromptMode
        priority_interface_list = None
        if args.interface:
            # If single value (str), wrap in list; if repeated (list), use as-is
            interfaces = [args.interface] if isinstance(args.interface, str) else args.interface
            try:
                priority_interface_list = [interface_mode_map[mode.lower()] for mode in interfaces]
            except KeyError as e:
                print(f"Error: Invalid interface mode '{e.args[0]}'")
                sys.exit(1)

        # Same for --avoid (order doesn't matter, so set)
        avoid_interface_set = None
        if args.avoid:
            avoids = [args.avoid] if isinstance(args.avoid, str) else args.avoid
            try:
                avoid_interface_set = {interface_mode_map[mode.lower()] for mode in avoids}
            except KeyError as e:
                print(f"Error: Invalid avoid mode '{e.args[0]}'")
                sys.exit(1)

       
        message_used = args.message_flag or args.message or "Enter value"

        exit_code = run_prompt(
            message=message_used,
            suggestion=args.suggestion,
            hide_input=args.hide,
            debug=args.debug,
            verbose=args.verbose,
            priority_interface=priority_interface_list,
            avoid_interface=avoid_interface_set,
        )
        sys.exit(exit_code)

    # No subcommand → show root help (exact Typer behavior)
    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
