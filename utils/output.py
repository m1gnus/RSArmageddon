import sys
import colorama
from colorama import Fore


def _print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)


colorama.init(autoreset=True)


def yellow(msg):
    _print(f"{Fore.YELLOW}{msg}")


def white(msg):
    _print(f"{Fore.LIGHTWHITE_EX}{msg}")


def success(msg):
    _print(f"[{Fore.GREEN}+{Fore.RESET}] {msg}")


def primary(msg):
    _print(f"[{Fore.BLUE}*{Fore.RESET}] {msg}")


def secondary(msg):
    _print(f"[{Fore.CYAN}#{Fore.RESET}] {msg}")


def info(msg):
    _print(f"[{Fore.BLUE}${Fore.RESET}] {msg}")


def warning(msg):
    _print(f"[{Fore.LIGHTYELLOW_EX}W{Fore.RESET}] {msg}")


def error(msg):
    _print(f"[{Fore.RED}-{Fore.RESET}] {msg}")


def newline():
    _print()


if __name__ == "__main__":
    yellow("Yellow text")
    white("White text")
    success("Success")
    primary("Primary output")
    secondary("Secondary output")
    info("Info")
    warning("Warning")
    error("Error")
