import sys
import colorama
from colorama import Fore


def _print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)


colorama.init(autoreset=True)


def yellow(msg, newline=True):
    _print(f"{Fore.YELLOW}{msg}", end=("\n" if newline else ""))


def white(msg, newline=True):
    _print(f"{Fore.LIGHTWHITE_EX}{msg}", end=("\n" if newline else ""))


def success(msg, newline=True):
    _print(f"[{Fore.GREEN}+{Fore.RESET}] {msg}", end=("\n" if newline else ""))


def primary(msg, newline=True):
    _print(f"[{Fore.CYAN}*{Fore.RESET}] {msg}", end=("\n" if newline else ""))


def secondary(msg, newline=True):
    _print(f"[{Fore.MAGENTA}#{Fore.RESET}] {msg}", end=("\n" if newline else ""))


def info(msg, newline=True):
    _print(f"[{Fore.BLUE}${Fore.RESET}] {msg}", end=("\n" if newline else ""))


def warning(msg, newline=True):
    _print(f"[{Fore.LIGHTYELLOW_EX}W{Fore.RESET}] {msg}", end=("\n" if newline else ""))


def error(msg, newline=True):
    _print(f"[{Fore.RED}-{Fore.RESET}] {msg}", end=("\n" if newline else ""))


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
