# src/dworshak_prompt/cli_stdlib.py
import sys
import argparse
from .multiplexer import DworshakPrompt, PromptMode, PromptCancelled
from .console_prompt_stdlib import stdlib_notify

def main():
    parser = argparse.ArgumentParser(
        prog="dworshak-prompt",
        description="Multiplexed user input via console/GUI/web",
        epilog="Falls back to basic stdlib input when Typer/Rich unavailable.",
    )
    parser.add_argument(
        "message",
        nargs="?",
        default="Enter value",
        help="The prompt message to display",
    )
    parser.add_argument(
        "--suggestion",
        "-s",
        default=None,
        help="Suggested/default value",
    )
    parser.add_argument(
        "--hide",
        "-H",
        action="store_true",
        help="Hide input (password mode)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    # Add more flags as needed (priority, avoid modes, etc.)

    args = parser.parse_args()

    if args.debug:
        import logging
        logging.getLogger("dworshak_prompt").setLevel(logging.DEBUG)

    try:
        value = DworshakPrompt.ask(
            message=args.message,
            suggestion=args.suggestion,
            hide_input=args.hide,
            debug=args.debug,
        )
        if value is not None:
            print(value)
        else:
            stdlib_notify("Input cancelled or no method succeeded.")
            sys.exit(1)

    except PromptCancelled:
        stdlib_notify("Prompt cancelled by user.")
        sys.exit(130)  # common Ctrl+C exit code
    except KeyboardInterrupt:
        stdlib_notify("Interrupted.")
        sys.exit(130)
    except Exception as e:
        stdlib_notify(f"Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
