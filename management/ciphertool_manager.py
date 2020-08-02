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

    if args.plaintext: # --plaintext <plaintext>

        """
        if a key is provided, then the values will be taken from the keys, else the values will be taken from -n and -e
        """
        if args.key:
            vals = dump_values_from_key(args.key)
            n, e = vals[:2]
        else:
            check_required(args.n, args.e)
            n, e = wrap_int_filter(args.n), wrap_int_filter(args.e)
        
        if args.padding:
            args.padding = validate_padding(args.padding)

        rsa_cipher_string(plaintext_filter(args.plaintext), n ,e, args.padding)

    if args.plaintext_file: # --plaintext-file <str>

        """
        openssl (which require a key file) is used, so if a key is not specified, we will create a temporary key (that will be deleted at the end of operation)
        """
        if not args.key:
            check_required(args.n, args.e)
            args.key = "/tmp/tmppubkey_RSArmageddon.pub"
            create_pubkey(wrap_int_filter(args.n), wrap_int_filter(args.e), "/tmp/tmppubkey_RSArmageddon.pub")
        else:
            validate_pubkey(args.key) # check that the key is a public key

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

    if args.ciphertext: # --ciphertext <ciphertext>
        if args.key:
            validate_privkey(args.key) # check that the key is a private key
            vals = dump_values_from_key(args.key)
            n, e, p, q, d = vals[:5]
        else:
            """
            If p and q are provided, then n is calculated
            """
            if args.p and args.q and not args.n:
                args.n = wrap_int_filter(args.p) * wrap_int_filter(args.q)

            """
            Is possible to uncipher a ciphertext by having only n and d
            """
            if args.n and args.d:
                n, d = wrap_int_filter(args.n), wrap_int_filter(args.d)

            else:
                """
                If d is not provided, is possible to recover it by n,e and phi
                """
                n, e = wrap_int_filter(args.n), wrap_int_filter(args.e)
                d = get_private_exponent(n, e, wrap_int_filter(args.phi))

                if not d:
                    """
                    If d is not recovered by n,e or phi (so n or e or phi is not provided) the software will try to create a full private key values set with "fill_privkey_args"
                    """
                    n, e, d, p, q = fill_privkey_args(n, e, wrap_int_filter(args.d), wrap_int_filter(args.p), wrap_int_filter(args.q))
        
        if args.padding:
            args.padding = validate_padding(args.padding)

        rsa_uncipher_string(ciphertext_filter(args.ciphertext), n, d, args.padding)

    if args.ciphertext_file: # --ciphertext-file <str>

        if not args.key:
            n, e, d, p, q = fill_privkey_args(wrap_int_filter(args.n), wrap_int_filter(args.e), wrap_int_filter(args.d), wrap_int_filter(args.p), wrap_int_filter(args.q))
            args.key = "/tmp/tmpprivkey_RSArmageddon.pub"
            create_privkey(n, e, d, p, q, "/tmp/tmpprivkey_RSArmageddon.pub", "PEM")
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
    
    if args.csubp == "cipher":
        cipher_manager(args)
    elif args.csubp == "uncipher":
        uncipher_manager(args)

