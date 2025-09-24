# hacker_protected.py
import signal
import sys

def ignore_exit(signum, frame):
    # Ignore Ctrl+C or kill attempts
    print("\033[91m[!] Nice try... system is protected.\033[0m")

# Ignore CTRL+C
signal.signal(signal.SIGINT, ignore_exit)

# On Unix (Linux/macOS), ignore terminal kill
try:
    signal.signal(signal.SIGHUP, ignore_exit)
    signal.signal(signal.SIGTERM, ignore_exit)
except Exception:
    pass  # Not always available on Windows

print("\033[92mSYSTEM LOCKED\033[0m")
print("Type the secret word to unlock...")

# Infinite loop until secret word is typed
while True:
    try:
        cmd = input("\033[92m>> \033[0m")
        if cmd.strip().lower() == "hello":
            print("\033[96mACCESS GRANTED. Shutting down...\033[0m")
            sys.exit(0)
        else:
            print("\033[91mACCESS DENIED. Try again.\033[0m")
    except Exception:
        print("\033[91mNice try, but you can't kill me like that...\033[0m")
