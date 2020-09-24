#!/usr/bin/env python3

import sys

import args
import banner

#from management.general_features import *
#from management.pem_manipulation import *
#from management.ciphertool_manager import *
#from management.attacks_manager import *

#from misc.signal_handler import *


general_features_manager = lambda: None
pem_manipulation_manager = lambda: None
ciphertool_manager = lambda: None
attack_manager = lambda: None


def main():
    banner.print()

    actions = {
        None: general_features_manager,
        "pem": pem_manipulation_manager,
        "ciphertool": ciphertool_manager,
        "attack": attack_manager
    }

    try:
        args.parse()
    except ValueError as e:
        print(f"[-] {e}", file=sys.stderr)
        sys.exit(1)

    actions[args.args.subp]()


if __name__ == "__main__":
    main()
