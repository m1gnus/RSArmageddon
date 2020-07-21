#!/usr/local/bin/sage --python

from banner import banner

from parsing.parser_config import *

from management.general_features import *
from management.pem_manipulation import *

if __name__ == "__main__":

    banner()

    if not args.subp:
        general_features_manager(args)
    elif args.subp == 'pem':
        pem_manipulation_manager(args)


