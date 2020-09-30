#!/usr/bin/env python3

import sys

from args import get_args

import banner

from commands import pem, ciphertool


#from misc.signal_handler import *


general_features_manager = lambda: None
attack_manager = lambda: None


def main():
    banner.print()

    actions = {
        None: general_features_manager,
        "pem": pem.run,
        "ciphertool": ciphertool.run,
        "attack": attack_manager
    }

    actions[get_args().subp]()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as e:
        print(f"[-] {e}", file=sys.stderr)
    except KeyboardInterrupt:
        print("[-] Interrupted")
    #except Exception as e:
    #    print(f"[E] Unhandled exception: {e}")
    else:
        sys.exit(0)

    sys.exit(1)
