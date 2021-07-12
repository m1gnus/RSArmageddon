#!/usr/bin/env python3

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


__version__ = "2.1.1"
__codename__ = "Ares"


import os
import sys

from functools import partial
from itertools import compress

from .utils import output
from .args import args
from .banner import (
        print_banner,
        print_credits,
        print_attacks,
        print_attacks_short,
        print_encodings,
        version)
from .commands import pem, ciphertool, attack, misc


def rsarmageddon():
    args.parse()
    output.init(args.color)

    if args.quiet:
        sys.stderr.close()
        sys.stderr = open(os.devnull, "w")

    if not any((args.show_attacks_short, args.show_encodings, args.version)):
        print_banner()

    banner_actions = compress(*zip(
        (partial(version, __version__, __codename__), args.version),
        (print_credits, args.credits),
        (print_attacks, args.show_attacks),
        (print_attacks_short, args.show_attacks_short),
        (print_encodings, args.show_encodings)
    ))

    try:
        action = next(banner_actions)
    except StopIteration:
        pass
    else:
        action()
        return

    if not args.command:
        return

    commands = {
        "pem": pem.run,
        "encrypt": ciphertool.run,
        "decrypt": ciphertool.run,
        "attack": attack.run
    }

    command = commands.get(args.command, misc.run)

    try:
        command()
    except (ValueError, OSError) as e:
        output.error(e)


def main():
    try:
        rsarmageddon()
    except RuntimeError as e:
        output.error(e)
    except KeyboardInterrupt:
        output.error("Interrupted")
    else:
        sys.exit(0)

    sys.exit(1)


if __name__ == "__main__":
    main()
