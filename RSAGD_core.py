#!/usr/bin/env python3

from banner import banner

from parsing.parser_config import *

from management.general_features import *
from management.pem_manipulation import *
from management.ciphertool_manager import *
from management.attacks_manager import *

from misc.signal_handler import *

if __name__ == "__main__":

    banner()

    if not args.subp:
        general_features_manager(args)
    elif args.subp == "pem":
        pem_manipulation_manager(args)
    elif args.subp == "ciphertool":
        ciphertool_manager(args)
    elif args.subp == "attack":
        attack_manager(args)
