"""
management of PEM manipulation options
"""
import sys

from parsing.args_filter import *
from pem_utils.certs_manipulation import *

def pem_manipulation_manager(args: object) -> None:
    if args.dumpvalues:
        check_required(args.key_path)
        dump_values_from_key(args.key_path)
    if args.cpub:
        check_required(args.n, args.e)
        create_pubkey(wrap_int_filter(args.n), wrap_int_filter(args.e), args.opub)
    