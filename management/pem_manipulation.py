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
    if args.cpriv:
        create_privkey(args.n, args.e, args.d, args.p, args.q, args.opriv)
    if args.generatekeypair:
        e = (wrap_int_filter(args.e) if args.e else 65537)
        generate_keypair(e, args.opub, args.opriv)
    