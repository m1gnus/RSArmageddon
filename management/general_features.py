"""
management of general purpose features
"""
import sys

from parser.args_filter import *
from os import system

def general_features_manager(args: object) -> None:

    if args.tofactor:
        int_input = wrap_int_filter(args.tofactor)
        system("features/sage_factor.sage " + str(int_input))
        sys.exit(0)
    if args.tofactorwecm:
        int_input = wrap_int_filter(args.tofactorwecm)
        system("features/sage_ecm_factor.sage " + str(int_input))
        sys.exit(0)
    if args.tofactorwqsieve:
        int_input = wrap_int_filter(args.tofactorwqsieve)
        system("features/sage_qsieve_factor.sage " + str(int_input))
        sys.exit(0)