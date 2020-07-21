"""
management of PEM manipulation options
"""
import sys

from parsing.args_filter import *
from pem_utils.certs_manipulation import *

def pem_manipulation_manager(args: object) -> None:
    if dumpvalues:
        check_required(args.key_path)
        dump_values_from_pem(args.key_path)