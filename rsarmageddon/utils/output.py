##########################################################################
# RSArmageddon - RSA cryptography and cryptoanalysis toolkit             #
# Copyright (C) 2020,2021                                                #
# Vittorio Mignini a.k.a. M1gnus <vittorio.mignini@gmail.com>            #
# Simone Cimarelli a.k.a. Aquilairreale <aquilairreale@ymail.com>        #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

import sys
import colorama
from colorama import Fore


def _print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)


def init(color="auto"):
    if color == "auto":
        colorama.init()
    elif color == "always":
        colorama.init(strip=False)
    elif color == "never":
        colorama.init(strip=True, convert=False)
    else:
        raise ValueError(f"Bad color setting {color!r}")


def yellow(msg, newline=True):
    _print(f"{Fore.YELLOW}{msg}{Fore.RESET}", end=("\n" if newline else ""))


def white(msg, newline=True):
    _print(f"{Fore.LIGHTWHITE_EX}{msg}{Fore.RESET}", end=("\n" if newline else ""))


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
