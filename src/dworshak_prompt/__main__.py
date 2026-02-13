# src/dworshak_prompt/__main__.py
try:
    from .cli import app
    def run():
        app()
except ImportError:
    from .cli_stdlib import main as run

if __name__ == "__main__":
    run()
