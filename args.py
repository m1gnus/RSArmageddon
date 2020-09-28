import sys
import argparse
import binascii

from itertools import zip_longest
from pathlib import Path

from parsing import (
        parse_int_arg,
        parse_list,
        parse_int_list,
        validate_padding,
        validate_file_padding,
        validate_file_format,
        path_or_stdout)

from utils import compute_d, complete_privkey, compute_pubkey, DEFAULT_E
from certs import load_key, generate_key, infer_format_priv, infer_format_pub


# Setting up the parser:
#     argument parsing will be organized in different subparsers
#     in order to improve readability and usability.
parser = argparse.ArgumentParser(add_help=True)
subparser = parser.add_subparsers(dest="subp")

# Attacks management
attacks_parser = subparser.add_parser("attack", add_help=True)

attacks_parser.add_argument("-n", action="store", dest="n", type=parse_int_list, default=None, help="List of RSA public modules <int>,<int>,<int>...")
attacks_parser.add_argument("-e", action="store", dest="e", type=parse_int_list, default=None, help="List of RSA public exponents <int>,<int>,<int>...")
attacks_parser.add_argument("--n-e-file", action="store", dest="n_e_file", type=Path, default=None, help='Path to a file containing modules and public exponents, each lines is in the form "n:e" or "n"')
attacks_parser.add_argument("--timeout", action="store", dest="timeout", type=parse_int_arg, default=None, help="Max elaboration time for attacks (seconds)")
attacks_parser.add_argument("--attack", action="store", dest="attacks", type=parse_list, default=None, help="List of attacks that will be performed <str>,<str>,<str>,...")
attacks_parser.add_argument("--ext", action="store", dest="exts", type=parse_list, default=["pem", "pub"], help="Extension of public keys in the folder specified by --publickeydir")
attacks_parser.add_argument("--private", action="store_true", dest="private", help="Dump private key file in PEM format if recovered")
attacks_parser.add_argument("--publickey", action="append", dest="publickey", type=Path, default=[], help="Path to a public key file")
attacks_parser.add_argument("--publickeydir", action="append", dest="publickey_dir", type=Path, default=[], help="Path to a folder containing public key files with extension ")
attacks_parser.add_argument("--uncipher", action="store", dest="ciphertext", type=parse_int_arg, default=None, help="Ciphertext to decrypt if the private key is recovered")
attacks_parser.add_argument("--uncipher-file", action="store", dest="ciphertext_file", type=Path, default=None, help="File to uncipher if the private key is recovered")
attacks_parser.add_argument("--output-private", action="store", dest="output_private", type=Path, default=None, help="Specify where to save the private key file in PEM format if the private key is recovered and --private flag is setted")
attacks_parser.add_argument("--output-file", action="store", dest="output_file", type=Path, default=Path.cwd()/"decrypted.dec", help='Specify where to save the decrypted file specified inn --uncipher-file if the private key is recovered (default: "./decrypted.dec")')
attacks_parser.add_argument("--output-dir", action="store", dest="output_dir", type=Path, default=None, help='Specify where to save the private key files recovered from the public keys specified (for attacks which requires more than one public key couple of values (default: ".")')


def _finalize_attacks_args(args):
    if args.output_private is not None:
        args.private = True
    args.pubkeys = []
    for i, (n, e) in enumerate(zip_longest(args.n, args.e)):
        if n is None:
            raise ValueError(f"Missing n value for e in position {i+1}")
        if e is None:
            e = DEFAULT_E
        args.pubkeys.append((n, e))
    if args.attacks is None:
        raise ValueError("Missing --attack flag")
    if not args.attacks:
        raise ValueError("--attack list is empty")


# Cipher tools
tools_parser = subparser.add_parser("ciphertool", add_help=True)
csubparser = tools_parser.add_subparsers(dest="csubp")

cipher_parser = csubparser.add_parser("cipher", add_help=True)
uncipher_parser = csubparser.add_parser("uncipher", add_help=True)

cipher_parser.add_argument("--key", action="store", dest="key", type=Path, default=None, help="Path to a public key file")
cipher_parser.add_argument("-n", action="store", dest="n", type=parse_int_arg, default=None, help="<int> which specify RSA public modulus")
cipher_parser.add_argument("-e", action="store", dest="e", type=parse_int_arg, default=None, help="<int> which specify RSA public exponent")
cipher_parser.add_argument("--plaintext", action="store", dest="plaintext", type=parse_int_arg, default=None, help="Takes an argument of <plaintext> type which represent the plaintext that will be encrypted with the given public key values")
cipher_parser.add_argument("--plaintext-string", action="store", dest="plaintext_str", type=str, default=None, help="Takes a string which represent the plaintext that will be encrypted with the given public key values")
cipher_parser.add_argument("--plaintext-file", action="store", dest="plaintext_file", type=Path, default=None, help="Path to a file wich represent the plaintext file that will be encrypted with the given public key values")
cipher_parser.add_argument("--file-padding", action="store", dest="filepadding", type=validate_file_padding, default="pkcs", help="Padding that will be used in the process for the given file (--plaintext-file), choose one of the follows: [raw, pkcs, ssl, oaep, x931] (default: pkcs)")
cipher_parser.add_argument("--padding", action="store", dest="padding", type=validate_padding, default=None, help="Padding that will be used in the process for the given plaintext (--plaintext), choose one from the follows: [pkcs7, iso7816, x923] (default: None)")
cipher_parser.add_argument("--output-file", action="store", dest="output_file", type=Path, default=None, help='Specify where to save the encrypted file (default: "PLAINTEXT_FILE.enc")')


def _finalize_cipher_args(args):
    if args.key is not None and args.n is not None:
        raise ValueError(f"--key and -n cannot be specified at the same time")
    if args.key is None and args.n is None:
        raise ValueError(f"Must specify either --key or -n")
    if args.n is not None and args.e is None:
        args.e = DEFAULT_E
    if args.plaintext is not None and args.plaintext_str is not None:
        raise ValueError(f"--plaintext and --plaintext_str cannot be specified at the same time")
    if all(arg is None for arg in (args.plaintext, args.plaintext_str, args.plaintext_file)):
        raise ValueError(f"Must specify at least one of --plaintext, --plaintext_str or --plaintext_file")
    if args.plaintext_str is not None:
        args.plaintext = int(binascii.hexlify(args.plaintext_str.encode()) or "0", 16)


uncipher_parser.add_argument("--key", action="store", dest="key", type=Path, default=None, help="Path to a private key file")
uncipher_parser.add_argument("-n", action="store", dest="n", type=parse_int_arg, default=None, help="<int> which specify RSA public modulus")
uncipher_parser.add_argument("-p", action="store", dest="p", type=parse_int_arg, default=None, help="<int> which specify RSA first prime factor")
uncipher_parser.add_argument("-q", action="store", dest="q", type=parse_int_arg, default=None, help="<int> which specify RSA second prime factor")
uncipher_parser.add_argument("-e", action="store", dest="e", type=parse_int_arg, default=None, help="<int> which specify RSA public exponent")
uncipher_parser.add_argument("-d", action="store", dest="d", type=parse_int_arg, default=None, help="<int> which specify RSA private exponent")
uncipher_parser.add_argument("-phi", "--phi", action="store", dest="phi", type=parse_int_arg, default=None, help="<int> which specify euler's phi of RSA public modulus")
uncipher_parser.add_argument("--ciphertext", action="store", dest="ciphertext", type=parse_int_arg, default=None, help="Takes an argument of <ciphertext> type which represent the ciphertext that will be decrypted with the given private key values")
uncipher_parser.add_argument("--ciphertext-file", action="store", dest="ciphertext_file", type=Path, default=None, help="Path to a file wich represent the ciphertext file that will be decrypted with the given private key values")
uncipher_parser.add_argument("--file-padding", action="store", dest="filepadding", type=validate_file_padding, default="pkcs", help="Padding that will be used in the process for the given file (--ciphertext-file), choose one of the follows: [raw, pkcs, ssl, oaep, x931] (default: pkcs)")
uncipher_parser.add_argument("--padding", action="store", dest="padding", type=validate_padding, default=None, help="Padding that will be used in the process for the given ciphertext (--ciphertext), choose one from the follows: [pkcs7, iso7816, x923] (default: None)")
uncipher_parser.add_argument("--output-file", action="store", dest="output_file", type=Path, default=None, help='Specify where to save the decrypted file (default: "PLAINTEXT_FILE.dec")')


def _finalize_uncipher_args(args):
    if args.ciphertext_file:
        args.n, args.e, args.d, args.p, args.q = complete_privkey(args.n, args.e, args.d, args.p, args.q)
    if args.ciphertext:
        args.d = compute_d(args.n, args.e, args.d, args.p, args.q, args.phi)


# PEM manipulation
pem_parser = subparser.add_parser("pem", add_help=True)


pem_parser.add_argument("--key", action="store", dest="key_path", type=Path, default=None, help="Path to a public/private key file")
pem_parser.add_argument("-n", action="store", dest="n", type=parse_int_arg, default=None, help="<int> which specify RSA public modulus")
pem_parser.add_argument("-p", action="store", dest="p", type=parse_int_arg, default=None, help="<int> which specify RSA first prime factor")
pem_parser.add_argument("-q", action="store", dest="q", type=parse_int_arg, default=None, help="<int> which specify RSA second prime factor")
pem_parser.add_argument("-e", action="store", dest="e", type=parse_int_arg, default=None, help="<int> which specify RSA public exponent")
pem_parser.add_argument("-d", action="store", dest="d", type=parse_int_arg, default=None, help="<int> which specify RSA private exponent")
pem_parser.add_argument("--dumpvalues", action="store_true", dest="dumpvalues", help="Dump numeric values from the given public/private key file (--key)")
pem_parser.add_argument("--createpub", action="store", dest="cpub", type=path_or_stdout, default=None, help="Create a public key file in the specified format (--file-format) from numeric values")
pem_parser.add_argument("--createpriv", action="store", dest="cpriv", type=path_or_stdout, default=None, help="Create a private key file in the specified format (--file-format) from numeric values")
pem_parser.add_argument("--generate", action="store_true", dest="generatekeypair", help="Generate a new key pair")
pem_parser.add_argument("--file-format", action="store", dest="format", type=validate_file_format, default=None, help="Specify the key file format, choose one from the follows: [PEM, DER, OpenSSH] (default: PEM)")


def _finalize_pem_args(args):
    if args.generatekeypair:
        if any(x is not None for x in (args.n, args.e, args.d, args.p, args.q, args.key_path)):
            print("[W] --generate taking precedence over any other options", file=sys.stderr) 
        args.n, args.e, args.d, args.p, args.q = generate_key()
    elif args.key_path is not None:
        if any(x is not None for x in (args.n, args.e, args.d, args.p, args.q)):
            print("[W] --key taking precedence over key element parameters when specified at the same time", file=sys.stderr)
        args.n, args.e, args.d, args.p, args.q = load_key(args.key_path)   
    else: # try to recover all the key elements
        try:
            args.n, args.e, args.d, args.p, args.q = complete_privkey(args.n, args.e, args.d, args.p, args.q)
        except ValueError:
            print("[W] Unable to compute private key from given values", file=sys.stderr)
            try:
                args.n, args.e, args.d, args.p, args.q = compute_pubkey(args.n, args.e, args.d, args.p, args.q)
            except ValueError:
                print("[W] Unable to compute public key from given values", file=sys.stderr)

    priv_fmt, pub_fmt = None, None

    if args.cpub is not None:
        if any(x is None for x in (args.n, args.e)):
            raise ValueError(f"--createpub and require a valid public key")
        priv_fmt = infer_format_priv(args.cpriv)
        
    if args.cpriv is not None:
        if any(x is None for x in (args.p, args.q, args.d)):
            raise ValueError(f"--createpriv and require a valid private key")
        pub_fmt = infer_format_pub(args.cpub)

    if args.format is None and any(x is not None for x in (args.cpriv, args.cpub)):
        fmts = set(filter(None, (priv_fmt, pub_fmt)))
        if len(fmts) >= 2:
            print("[W] Different formats inferred for private and public key output. Using private key format for both", file=sys.stderr)
        if len(fmts) >= 1:
            args.format = priv_fmt if priv_fmt is not None else pub_fmt
        else:
            print("[W] Output file format could not be inferred. Defaulting to 'pem'", file=sys.stderr)
            args.format = "PEM"



# General features
parser.add_argument("--factor", action="store", dest="tofactor", type=parse_int_arg, default=None, help="<int> to factorize with pari's factor")
parser.add_argument("--ecm", action="store", dest="tofactorwecm", type=parse_int_arg, default=None, help="<int> to factorize with ecm factorization")
parser.add_argument("--qs", action="store", dest="tofactorwqsieve", type=parse_int_arg, default=None, help="<int> to factorize with quadratic sieve method")
parser.add_argument("--isprime", action="store", dest="checkprime", type=parse_int_arg, default=None, help="Check if the given <int> is prime")
parser.add_argument("--eulerphi", action="store", dest="n_phi", type=parse_int_arg, default=None, help="<int> of which calc euler phi")
parser.add_argument("--show-attacks", action="store_true", dest="showattacks", help="Show implemented attacks")
parser.add_argument("--credits", action="store_true", dest="showcredits", help="Show credits")
parser.add_argument("--version", action="store_true", dest="showversion", help="Show version")


def _finalize_general_args(args):
    if len([x for x in vars(args).values() if x not in (None, False)]) > 1:
        raise ValueError(f"Only one argument at a time can be specified without a command")


args = None


def get_args():
    """Run args parser
    """
    global args

    if args is not None:
        return args

    finalize = {
        "attack": _finalize_attacks_args,
        "cipher": _finalize_cipher_args,
        "uncipher": _finalize_uncipher_args,
        "pem": _finalize_pem_args,
        None: _finalize_general_args
    }

    args = parser.parse_args()
    finalize[args.csubp if args.subp == "ciphertool" else args.subp](args)

    return args