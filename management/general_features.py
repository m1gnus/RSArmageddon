"""
management of general purpose features
"""
import sys
from os import system

from banner import *
from parser.args_filter import *

def general_features_manager(args: object) -> None:

    if args.tofactor: # --factor <int>
        int_input = wrap_int_filter(args.tofactor)
        system("features/sage_factor.sage " + str(int_input))
        sys.exit(0)
    if args.tofactorwecm: # --ecm <int>
        int_input = wrap_int_filter(args.tofactorwecm)
        system("features/sage_ecm_factor.sage " + str(int_input))
        sys.exit(0)
    if args.tofactorwqsieve: # --qsieve <int>
        int_input = wrap_int_filter(args.tofactorwqsieve)
        system("features/sage_qsieve_factor.sage " + str(int_input))
        sys.exit(0)
    if args.checkprime: # --isprime <int>
        int_input = wrap_int_filter(args.checkprime)
        system("features/sage_isprime.sage " + str(int_input))
        sys.exit(0)
    if args.showversion:
        version()
        sys.exit(0)
    if args.showcredits: # --credits
        credits()
        sys.exit(0)
    if args.showattacks: # --show-attacks
        show_attacks()
        sys.exit(0)
