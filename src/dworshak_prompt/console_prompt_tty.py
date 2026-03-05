# src/dworshak_prompt/console_prompt_tty.py
import os
import sys
from .keyboard_interrupt import PromptCancelled

def tty_prompt(message: str, suggestion: str | None = None, hide_input: bool = False) -> str:
    try:
        tty_in = open("/dev/tty", "r")
        tty_out = open("/dev/tty", "w")
    except OSError:
        raise PromptCancelled()

    prompt = message
    if suggestion:
        prompt += f" [{suggestion}]"
    prompt += ": "

    try:
        if hide_input:
            import termios, tty as ttymod
            print(prompt, file=tty_out, flush=True)
            fd = tty_in.fileno()
            old = termios.tcgetattr(fd)
            try:
                ttymod.setraw(fd)
                buf = []
                while True:
                    ch = tty_in.read(1)

                    # Handle Enter/Return
                    if ch in ("\n", "\r"):
                        break
                    # Handle Ctrl+C (Interrupt)
                    if ch == "\x03":
                        raise KeyboardInterrupt
                    
                    # Handle Backspace (\x7f is modern, \x08 is legacy)
                    if ch in ("\x7f", "\x08"):
                        if buf:
                            buf.pop()
                            # If you were echoing asterisks, you'd need to 
                            # print "\b \b" to tty_out here. 
                            # Since we are totally hidden, we just pop the list.
                        continue

                    # Handle Ctrl+D (EOF)
                    if ch == "\x04":
                        if not buf:
                            raise EOFError
                        break

                    buf.append(ch)
                print(file=tty_out)
                return "".join(buf)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        else:
            print(prompt, file=tty_out, flush=True)
            val = tty_in.readline()
            if not val:
                raise PromptCancelled()
            val = val.rstrip("\n")
            return val or suggestion
    except (KeyboardInterrupt, EOFError):
        raise PromptCancelled()
