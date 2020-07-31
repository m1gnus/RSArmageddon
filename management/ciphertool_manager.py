"""
management of cipher/uncipher options
"""
import sys

from parsing.args_filter import *

from pem_utils.certs_manipulation import dump_values_from_key, create_pubkey

from cipher_tools.cipher import *
from cipher_tools.uncipher import *

from misc.signal_handler import *

def cipher_manager(args: object) -> None:

    if args.plaintext:

        if args.key:
            vals = dump_values_from_key(args.key)
            n, e = vals[:2]
        else:
            check_required(args.n, args.e)
            n, e = wrap_int_filter(args.n), wrap_int_filter(args.e)
        
        if args.padding:
            args.padding = validate_padding(args.padding)

        rsa_cipher_string(plaintext_filter(args.plaintext), n ,e, args.padding)

    if args.plaintext_file:

        if not args.key:
            check_required(args.n, args.e)
            args.key = "/tmp/tmppubkey_RSArmageddon.pub"
            create_pubkey(wrap_int_filter(args.n), wrap_int_filter(args.e), "/tmp/tmppubkey_RSArmageddon.pub")
        else:
            validate_pubkey(args.key)

        files = list_filter(args.plaintext_file)
        outnames = list_filter(args.output_file)

        args.filepadding = validate_padding_for_file(args.filepadding)

        while files:
            file_ = files.pop(0)
            outname = outnames.pop(0) if outnames else (file_ + ".enc")
            rsa_cipher_file(file_, outname, args.key, args.filepadding)

        if args.key == "/tmp/tmppubkey_RSArmageddon.pub":
            system("rm -rf /tmp/tmppubkey_RSArmageddon.pub")
        

def uncipher_manager(args: object) -> None:

    if args.ciphertext:
        if args.key:
            validate_privkey(args.key)
            vals = dump_values_from_key(args.key)
            n, e, p, q, d = vals[:5]
        else:
            n, e, d, p, q = fill_privkey_args(wrap_int_filter(args.n), wrap_int_filter(args.e), wrap_int_filter(args.d), wrap_int_filter(args.p), wrap_int_filter(args.q))
        
        if args.padding:
            args.padding = validate_padding(args.padding)

        rsa_uncipher_string(ciphertext_filter(args.ciphertext), n, d, args.padding)

    if args.ciphertext_file:

        if not args.key:
            n, e, d, p, q = fill_privkey_args(wrap_int_filter(args.n), wrap_int_filter(args.e), wrap_int_filter(args.d), wrap_int_filter(args.p), wrap_int_filter(args.q))
            args.key = "/tmp/tmpprivkey_RSArmageddon.pub"
            create_privkey(n, e, d, p, q, "/tmp/tmpprivkey_RSArmageddon.pub", 'PEM')
        else:
            validate_privkey(args.key)

        files = list_filter(args.ciphertext_file)
        outnames = list_filter(args.output_file)

        args.filepadding = validate_padding_for_file(args.filepadding)

        while files:
            file_ = files.pop(0)
            outname = outnames.pop(0) if outnames else (file_ + ".dec")
            rsa_uncipher_file(file_, outname, args.key, args.filepadding)

        if args.key == "/tmp/tmpprivkey_RSArmageddon.pub":
            system("rm -rf /tmp/tmpprivkey_RSArmageddon.pub")

def ciphertool_manager(args: object) -> None:
    
    if args.csubp == 'cipher':
        cipher_manager(args)
    elif args.csubp == 'uncipher':
        uncipher_manager(args)

