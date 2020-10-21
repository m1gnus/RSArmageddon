#!/usr/bin/env python3


import os
import sys

from banner import print_banner
from args import args
from commands import pem, ciphertool, attack, misc


def main():
    if args.quiet:
        sys.stderr.close()
        sys.stderr = open(os.devnull, "w")

    banner_actions = compress(zip(
        (version, args.version),
        (credits, args.credits),
        (print_attacks, args.print_attacks),
        (print_attacks_short, args.print_attacks_short)
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
        "ciphertool": ciphertool.run,
        "attack": attack.run
    }

    action = actions.get(args.command, misc.run)

    try:
        action()
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
