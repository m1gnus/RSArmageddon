#!/usr/bin/env python3

from banner import banner

from args import args

from management.general_features import *
from management.pem_manipulation import *
from management.ciphertool_manager import *
from management.attacks_manager import *

from misc.signal_handler import *


def main():
    banner()

    actions = {
        "": general_features_manager,
        "pem": pem_manipulation_manager,
        "ciphertool": ciphertool_manager,
        "attack": attack_manager
    }

    actions[args.subp]()


if __name__ == "__main__":
    main()
