#!/usr/bin/env python3


import os
import sys

from itertools import compress

from args import args
from banner import (
        print_banner,
        print_credits,
        print_attacks,
        print_attacks_short,
        version)
from commands import pem, ciphertool, attack, misc


def main():
    if args.quiet:
        sys.stderr.close()
        sys.stderr = open(os.devnull, "w")

    print_banner()

    banner_actions = compress(*zip(
        (version, args.version),
        (credits, args.credits),
        (print_attacks, args.show_attacks),
        (print_attacks_short, args.show_attacks_short)
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
        print(f"[-] {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[-] Interrupted")
    #except Exception as e:
    #    print(f"[E] Unhandled exception: {e}")
    else:
        sys.exit(0)

    sys.exit(1)
