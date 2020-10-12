#!/usr/bin/env python3


import os
import sys

from banner import print_banner
from args import get_args
from commands import pem, ciphertool, attack, default


def main():
    try:
        args = get_args()
    except (ValueError, OSError) as e:
        print(f"[-] {e}", file=sys.stderr)
        return

    if args.quiet:
        sys.stderr.close()
        sys.stderr = open(os.devnull, "w")

    print_banner()

    actions = {
        None: default.run,
        "pem": pem.run,
        "ciphertool": ciphertool.run,
        "attack": attack.run
    }

    actions[args.subp]()


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
