#!/usr/local/bin/sage --python

from parser.parser_config import *

from management.general_features import *

if __name__ == "__main__":

    if not args.subp:
        general_features_manager(args)        


