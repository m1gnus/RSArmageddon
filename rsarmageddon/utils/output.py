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


def init(color="auto"):
    if color == "auto":
        colorama.init()
    elif color == "always":
        colorama.init(strip=False)
    elif color == "never":
        colorama.init(strip=True, convert=False)
    else:
        raise ValueError(f"Bad color setting {color!r}")


def newline():
    print(file=sys.stderr)


def _print(*args, **kwargs):
    print(*args, **kwargs, end="", file=sys.stderr)


def make_output(name, color=Fore.RESET, widget=None, widget_color=None):
    if widget_color is None:
        widget_color = ""

    widget_text = ""
    indent = 0
    if widget is not None:
        widget_text = f"[{widget_color}{widget}{Fore.RESET}] "
        indent = len(widget) + 3

    def output(msg, newline=True):
        msg = str(msg)
        lines = iter(msg.splitlines() or [""])

        firstline = next(lines)
        _print(widget_text)
        _print(f"{color}{firstline}")

        for line in lines:
            _print("\n")
            _print(" " * indent)
            _print(f"{line}")

        _print(Fore.RESET)

        if newline:
            _print("\n")

        sys.stderr.flush()

    output.__name__ = name
    return output


yellow = make_output("yellow", Fore.YELLOW)
white = make_output("white", Fore.LIGHTWHITE_EX)
success = make_output("success", widget="+", widget_color=Fore.GREEN)
primary = make_output("primary", widget="*", widget_color=Fore.CYAN)
secondary = make_output("secondary", widget="#", widget_color=Fore.MAGENTA)
info = make_output("info", widget="$", widget_color=Fore.BLUE)
warning = make_output("warning", widget="W", widget_color=Fore.LIGHTYELLOW_EX)
error = make_output("error", widget="-", widget_color=Fore.RED)


if __name__ == "__main__":
    init(color="always")
    yellow("Yellow text")
    white("White text")
    success("Success")
    primary("Primary output")
    secondary("Secondary output")
    info("Info")
    warning("Warning")
    error("Error")
    newline()
    yellow("Multiline\nyellow")
    white("Multiline\nwhite")
    success("Multiline\nsuccess")
    primary("Multiline\nprimary output")
    secondary("Multiline\nsecondary output")
    info("Multiline\ninfo")
    warning("Multiline\nwarning")
    error("Multiline\nerror")
