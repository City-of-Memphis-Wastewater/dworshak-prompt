# src/dworshak_prompt/cli_stdlib.py
import argparse
import sys

from .multiplexer import DworshakPrompt, PromptMode
from .keyboard_interrupt import PromptCancelled
from .console_prompt_stdlib import stdlib_notify
from ._version import __version__

def run_prompt(
    message: str = "Enter value",
    suggestion: str | None = None,
    hide_input: bool = False,
    debug: bool = False,
    priority: list[PromptMode] | None = None,
) -> int:
    if debug:
        import logging
        logging.getLogger("dworshak_prompt").setLevel(logging.DEBUG)

    try:
        value = DworshakPrompt.ask(
            message=message,
            suggestion=suggestion,
            hide_input=hide_input,
            priority=priority,
            debug=debug,
        )
        if value is not None:
            print(value)
            return 0
        else:
            stdlib_notify("Input cancelled or no method succeeded.")
            return 1

    except PromptCancelled:
        stdlib_notify("Prompt cancelled by user.")
        return 130
    except KeyboardInterrupt:
        stdlib_notify("Interrupted.")
        return 130
    except Exception as e:
        stdlib_notify(f"Error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return 1


def main():
    parser = argparse.ArgumentParser(
        prog="dworshak-prompt",
        description=f"Multiplexed user input via console, GUI, and web. (v{__version__})",
        add_help=False,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=False,
        help="Available commands",
    )

    # ask subcommand – exact match in name, help text, flags
    ask_parser = subparsers.add_parser(
        "ask",
        help="Get user input and print it to stdout",
        description="Prompt the user using available methods.",
        add_help=False,
    )

    ask_parser.add_argument(
        "--message",
        "-m",
        default="Enter value",
        help="The prompt message to display",
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
        "--mode",
        choices=[m.value for m in PromptMode], 
        default=PromptMode.CONSOLE.value,
        type=str.lower,
        help="Preferred input mode (case-insensitive)",
    )
    ask_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
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
        mode_map = {m.value: m for m in PromptMode}
        selected_mode = mode_map[args.mode]

        exit_code = run_prompt(
            message=args.message,
            suggestion=args.suggestion,
            hide_input=args.hide,
            debug=args.debug,
            priority=[selected_mode],
        )
        sys.exit(exit_code)

    # No subcommand → show root help (exact Typer behavior)
    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
