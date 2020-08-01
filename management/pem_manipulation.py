"""
management of PEM manipulation options
"""
import sys

from parsing.args_filter import *
from pem_utils.certs_manipulation import *

from misc.signal_handler import *

def pem_manipulation_manager(args: object) -> None:
    if args.dumpvalues: # --dumpvalues
        check_required(args.key_path)
        dump_values_from_key(args.key_path)
    if args.generatekeypair: # --generate
        e = (wrap_int_filter(args.e) if args.e else 65537)
        generate_keypair(e, args.opub, args.opriv)
        sys.exit(0)
    if args.cpub: # --createpub
        check_required(args.n, args.e)
        create_pubkey(wrap_int_filter(args.n), wrap_int_filter(args.e), args.opub, args.format)
    if args.cpriv: # --createpriv
        create_privkey(wrap_int_filter(args.n), wrap_int_filter(args.e), wrap_int_filter(args.d), wrap_int_filter(args.p), wrap_int_filter(args.q), args.opriv, args.format)
    