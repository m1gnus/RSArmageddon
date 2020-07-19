"""
management of general purpose features
"""

from parser.args_filter import *
from os import system

def general_features_manager(args: object) -> None:
    if args.tofactor:
        int_input = wrap_int_filter(args.tofactor)
        system("features/sage_factor.py " + str(int_input))