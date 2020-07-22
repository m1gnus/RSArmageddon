"""
management of cipher/uncipher options
"""
import sys

from parsing.args_filter import *

from pem_utils.certs_manipulation import dump_values_from_pem, create_pubkey

from cipher_tools.cipher import *
from cipher_tools.uncipher import *

def cipher_manager(args: object) -> None:

    if args.plaintext:

        if args.key:
            n, e = dump_values_from_key(args.key)
        else:
            check_required(args.n, args.e)
            n, e = wrap_int_filter(args.n), wrap_int_filter(args.e)
        rsa_cipher_string(plaintext_filter(args.plaintext))

    if args.plaintext_file:

        if not args.key:
            check_required(args.n, args.e)
            args.key = "/tmp/tmppubkey_RSArmageddon.pub"
            create_pubkey(wrap_int_filter(args.n), wrap_int_filter(args.e), "/tmp/pub.pem")
        
        files = list_filter(args.plaintext_file)
        outnames = list_filter(args.output_file)

        while files:
            file_ = files.pop(0)
            outname = outnames.pop(0) if outnames else (file_ + ".enc")
            rsa_cipher_file(file_, outname, args.key)

        if args.key == "/tmp/tmppubkey_RSArmageddon.pub":
            system("rm -rf /tmp/tmppubkey_RSArmageddon.pub")
        

def uncipher_manager(args: object) -> None:
    pass

def ciphertool_manager(args: object) -> None:
    
    if args.csubp == 'cipher':
        cipher_manager(args)
    elif args.csubp == 'uncipher':
        cipher_manager(args)

