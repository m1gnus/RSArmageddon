#!/usr/bin/env python3

import os
import sys

from itertools import compress

from utils import output
from args import args
from banner import (
        print_banner,
        print_credits,
        print_attacks,
        print_attacks_short,
        print_encodings,
        version)
from commands import pem, ciphertool, attack, misc


def main():
    output.init(args.color)

    if args.quiet:
        sys.stderr.close()
        sys.stderr = open(os.devnull, "w")

    if not any((args.show_attacks_short, args.show_encodings, args.version)):
        print_banner()

    banner_actions = compress(*zip(
        (version, args.version),
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        output.error("Interrupted")
    #except Exception as e:
    #    output.error(f"Unhandled exception: {e}")
    else:
        sys.exit(0)

    sys.exit(1)
