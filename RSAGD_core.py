#!/usr/local/bin/sage --python

from banner import banner

from parser.parser_config import *

from management.general_features import *

if __name__ == "__main__":

    banner()

    if not args.subp:
        general_features_manager(args)        


