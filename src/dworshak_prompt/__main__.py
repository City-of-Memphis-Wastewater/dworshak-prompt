# src/dworshak_prompt/__main__.py
try:
    from .cli import app
    def run():
        app()
except ImportError:
    #from .cli_stdlib import main as run
    import sys
    #print("Please install this package with the 'typer' extra to utilize the CLI.", file=sys.stderr)
    # Fallback when dependencies are missing
    def run():
        print(
            "Please install this package with the 'typer' extra to utilize the CLI.",
            file=sys.stderr
        )
        sys.exit(1)
if __name__ == "__main__":
    run()
