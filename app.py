# hacker_countdown.py
# Simple "hacker-style" countdown: animated binary noise + typewriter reveal
# Works on Linux/macOS and modern Windows terminals (Windows 10+ with ANSI enabled)

import sys
import time
import random
import shutil
import os

# ANSI color codes
GREEN = "\033[92m"
DIM = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"  # clear screen and move cursor home

def term_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80

def noisy_banner(lines=8, density=0.08):
    """Generate a block of random binary/hex noise."""
    w = term_width()
    out = []
    for _ in range(lines):
        line = []
        for _ in range(w):
            if random.random() < density:
                line.append(random.choice("01"))
            else:
                line.append(" ")
        out.append("".join(line))
    return out

def typewriter_print(text, delay=0.02, end="\n"):
    """Typewriter effect."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay * (0.8 + random.random()*0.6))
    sys.stdout.write(end)
    sys.stdout.flush()

def center_text(text):
    w = term_width()
    lines = text.splitlines()
    centered = []
    for l in lines:
        pad = max((w - len(l)) // 2, 0)
        centered.append(" " * pad + l)
    return "\n".join(centered)

def print_big_count(n):
    """Simple big-ish number display (not figlet, but clear)."""
    s = f"""
     ██████   ██████   ██████
    █      █ █      █ █      █
    █  {str(n).rjust(2)}  █ █  {str(n).rjust(2)}  █ █  {str(n).rjust(2)}  █
    █      █ █      █ █      █
     ██████   ██████   ██████
    """.strip("\n")
    print(center_text(GREEN + s + RESET))

def progress_bar(pct, width=40):
    filled = int(width * pct)
    bar = "[" + "#" * filled + "-" * (width - filled) + "]"
    return bar

def hacker_countdown(start=10):
    os.system("")  # sometimes needed to enable ANSI on Windows
    # Intro flicker
    for _ in range(3):
        print(CLEAR, end="")
        noise = noisy_banner(lines=10, density=0.06)
        print(GREEN + "\n".join(noise) + RESET)
        time.sleep(0.12)
    # Stable intro
    print(CLEAR, end="")
    intro = center_text("INITIALIZING SECURE CHANNEL")
    print(GREEN + DIM + intro + RESET)
    time.sleep(0.7)

    # Countdown loop
    for i in range(start, 0, -1):
        # quick noise overlay
        for _ in range(2):
            print(CLEAR, end="")
            noise = noisy_banner(lines=8, density=0.04)
            print(GREEN + "\n".join(noise) + RESET)
            time.sleep(0.06)

        # Print big number
        print(CLEAR, end="")
        print(GREEN + DIM + center_text(">>> BOOT SEQUENCE <<<") + RESET)
        print()
        print_big_count(i)
        print()
        # progress animation
        for step in range(21):
            pct = step / 20.0
            line = center_text(f"{progress_bar(pct, width=30)}  {int(pct*100):3d}%")
            print("\r" + " " * (term_width()), end="")  # clear line
            sys.stdout.write("\033[s")  # save cursor pos
            # print centered progress (we print directly to not disturb big number)
            sys.stdout.write("\033[6B")  # move down to approximate place
            sys.stdout.write("\r" + GREEN + line + RESET)
            sys.stdout.write("\033[u")  # restore cursor pos
            sys.stdout.flush()
            time.sleep(0.03 + random.random()*0.02)
        # short pause between numbers
        time.sleep(0.25)

        # small reveal text
        print("\n")
        typewriter_print(GREEN + "    AUTHENTICATION TOKEN: " + "".join(random.choice("ABCDEF0123456789") for _ in range(16)) + RESET, delay=0.003)
        time.sleep(0.5)

    # Final message
    print(CLEAR, end="")
    for _ in range(4):
        noise = noisy_banner(lines=10, density=0.07)
        print(GREEN + "\n".join(noise) + RESET)
        time.sleep(0.08)
        print(CLEAR, end="")
    final = center_text("ACCESS GRANTED\n-- SYSTEM ONLINE --")
    typewriter_print(GREEN + final + RESET, delay=0.01)
    print()
    typewriter_print(GREEN + ">> Launch successful. Have fun, hacker." + RESET, delay=0.01)

if __name__ == "__main__":
    try:
        hacker_countdown(10)
    except KeyboardInterrupt:
        print(RESET + "\nInterrupted. Exiting.")
