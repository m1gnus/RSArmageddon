import sys
import colorama
from colorama import Fore


colorama.init(autoreset=True)


def yellow(msg):
    print(f"{Fore.YELLOW}{msg}", file=sys.stderr)


def white(msg):
    print(f"{Fore.LIGHTWHITE_EX}{msg}", file=sys.stderr)


def success(msg):
    print(f"[{Fore.GREEN}+{Fore.RESET}] {msg}", file=sys.stderr)


def primary(msg):
    print(f"[{Fore.BLUE}*{Fore.RESET}] {msg}", file=sys.stderr)


def secondary(msg):
    print(f"[{Fore.CYAN}#{Fore.RESET}] {msg}", file=sys.stderr)


def info(msg):
    print(f"[{Fore.BLUE}${Fore.RESET}] {msg}", file=sys.stderr)


def warning(msg):
    print(f"[{Fore.LIGHTYELLOW_EX}W{Fore.RESET}] {msg}", file=sys.stderr)


def error(msg):
    print(f"[{Fore.RED}-{Fore.RESET}] {msg}", file=sys.stderr)


def newline():
    print(file=sys.stderr)


if __name__ == "__main__":
    yellow("Yellow")
    white("White")
    success("Success")
    info("Info")
    warning("Warning")
    error("Error")
