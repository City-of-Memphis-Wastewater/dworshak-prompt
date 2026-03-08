# src/dworshak_prompt/console_prompt_tty.py
import os
import sys
from .keyboard_interrupt import PromptCancelled

def console_get_input_tty(message: str, suggestion: str | None = None, hide_input: bool = False) -> str:

    prompt = message
    if suggestion:
        prompt += f" [{suggestion}]"
    prompt += ": "

    try:
        with open("/dev/tty", "r") as tty_in, open("/dev/tty", "w") as tty_out:
            if hide_input:
                import termios, tty as ttymod
                #print(prompt, file=tty_out, flush=True)
                print(prompt, file=tty_out, flush=True, end="")
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
                print(prompt, file=tty_out, flush=True, end="")
                #print(prompt, file=tty_out, flush=True)
                val = tty_in.readline()
                if not val:
                    # print a newline so the next shell prompt isn't on the same line
                    print(file=tty_out, flush=True)
                    raise PromptCancelled()
                val = val.rstrip("\n")
                return val or suggestion
    except (KeyboardInterrupt, EOFError):
        raise PromptCancelled()
