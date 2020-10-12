import sys
import argparse
import binascii

from itertools import zip_longest
from functools import partial
from pathlib import Path

from parsing import (
        parse_int_arg,
        parse_list,
        parse_int_list,
        validate_padding,
        validate_file_format,
        path_or_stdout)

from utils import compute_d, complete_privkey, compute_pubkey, compute_n, DEFAULT_E
from certs import load_key, generate_key, infer_format_priv, infer_format_pub


# Setting up the parser:
#     argument parsing will be organized in different subparsers
#     in order to improve readability and usability.
parser = argparse.ArgumentParser(add_help=True)
subparser = parser.add_subparsers(dest="subp")

# Attacks management
attacks_parser = subparser.add_parser("attack", add_help=True)

#TODO
attacks_parser.add_argument("-n", action="store", dest="n", type=parse_int_list, default=[], help="List of RSA public modules <int>,<int>,<int>...")
attacks_parser.add_argument("-e", action="store", dest="e", type=parse_int_list, default=[], help="List of RSA public exponents <int>,<int>,<int>...")
attacks_parser.add_argument("--n-e-file", action="store", dest="n_e_file", type=Path, default=None, help='Path to a file containing modules and public exponents, each lines is in the form "n:e" or "n"')
attacks_parser.add_argument("--timeout", action="store", dest="timeout", type=parse_int_arg, default=None, help="Max elaboration time for attacks (seconds)")
attacks_parser.add_argument("--attacks", action="store", dest="attacks", type=parse_list, default=None, help="List of attacks that will be performed <str>,<str>,<str>,...")
attacks_parser.add_argument("--ext", action="store", dest="exts", type=parse_list, default=["pem", "pub"], help="Extension of public keys in the folder specified by --publickeydir")
attacks_parser.add_argument("--private", action="store_true", dest="private", help="Dump private key file in PEM format if recovered")
attacks_parser.add_argument("--publickey", action="append", dest="publickeys", type=Path, default=[], help="Path to a public key file")
attacks_parser.add_argument("--publickeydir", action="append", dest="publickey_dirs", type=Path, default=[], help="Path to a folder containing public key files with extension ")
attacks_parser.add_argument("--uncipher", "-u", action="append", dest="ciphertexts", type=parse_int_arg, default=[], help="Ciphertext to decrypt if the private key is recovered")
attacks_parser.add_argument("--uncipher-output", "--uo", action="append", dest="ciphertext_outputs", type=path_or_stdout, default=[], help="Ciphertext to decrypt if the private key is recovered")
attacks_parser.add_argument("--uncipher-file", "--uf", action="append", dest="ciphertext_files", type=Path, default=[], help="File to uncipher if the private key is recovered")
attacks_parser.add_argument("--uncipher-file-output", "--ufo", action="append", dest="ciphertext_file_outputs", type=path_or_stdout, default=[], help="File to uncipher if the private key is recovered")
attacks_parser.add_argument("--output-private", "--op", action="store", dest="output_private", type=path_or_stdout, default=None, help="Specify where to save the private key file in PEM format if the private key is recovered and --private flag is setted")
attacks_parser.add_argument("--output-dir", "--od", action="store", dest="output_dir", type=Path, default=None, help='Specify where to save the private key files recovered from the public keys specified (for attacks which requires more than one public key couple of values (default: ".")')
attacks_parser.add_argument("--standard", action="store", dest="padding", type=validate_padding, default="raw", help="Padding that will be used in the process for the given ciphertext (--ciphertext), choose one from the follows: [pkcs, oaep, raw] (default: raw)")
attacks_parser.add_argument("--json", "-j", action="store_true", dest="json", help="Make stdout outputs JSON")
attacks_parser.add_argument("--quiet", "--silent", "-s", action="store_true", dest="quiet", help='Suppress informative output')


def _finalize_attacks_args(args):
    if args.attacks is None:
        raise ValueError("Missing --attacks flag")
    if not args.attacks:
        raise ValueError("--attacks list is empty")
    args.pubkeys = []
    for i, (n, e) in enumerate(zip_longest(args.n, args.e)):
        if n is None:
            raise ValueError(f"Missing n value for e in position {i+1}")
        if e is None:
            e = DEFAULT_E
        args.pubkeys.append(((n, e), None))
    if args.n_e_file:
        args.pubkeys.extend((key, None) for key in parse_n_e_file(args.n_e_file))
    for filename in args.publickeys:
        n, e, _, _, _ = load_key(filename)
        args.pubkeys.append(((n, e), filename.name))
    for dirname in args.publickey_dirs:
        args.pubkeys.append(load_keys(dirname, args.exts))
    if not args.pubkeys:
        raise ValueError("Cannot perform any attack without at least one public key")
    if args.private and args.output_private is None:
        args.output_private = True
    texts = []
    for text in args.ciphertexts:
        if args.ciphertext_outputs:
            texts.append((text, args.ciphertext_outputs.pop(0)))
        else:
            texts.append((text, True))
    for text_file in args.ciphertext_files:
        with open(text_file, "rb") as f:
            text = int.from_bytes(f.read(), "big")
        if args.ciphertext_output_files:
            texts.append(text, args.ciphertext_output_files.pop(0))
        else:
            texts.append(text, f"{text_file.stem}.dec")
    args.ciphertexts = texts


# Cipher tools
tools_parser = subparser.add_parser("ciphertool", add_help=True)
csubparser = tools_parser.add_subparsers(dest="csubp")

cipher_parser = csubparser.add_parser("cipher", add_help=True)
uncipher_parser = csubparser.add_parser("uncipher", add_help=True)

cipher_parser.add_argument("--key", action="store", dest="key", type=Path, default=None, help="Path to a public key file")
cipher_parser.add_argument("-n", action="store", dest="n", type=parse_int_arg, default=None, help="<int> which specify RSA public modulus")
cipher_parser.add_argument("-e", action="store", dest="e", type=parse_int_arg, default=None, help="<int> which specify RSA public exponent")
cipher_parser.add_argument("--plaintext", "--pt", action="store", dest="inputs", type=parse_int_list, default=[], help="Takes an argument of <plaintext> type which represent the plaintext that will be encrypted with the given public key values")
cipher_parser.add_argument("--plaintext-output", "--po", action="append", dest="outputs", type=path_or_stdout, default=[], help='TODO')
cipher_parser.add_argument("--plaintext-string", "--ps", action="append", dest="input_strs", type=str, default=[], help="Takes a string which represent the plaintext that will be encrypted with the given public key values")
cipher_parser.add_argument("--plaintext-string-output", "--pso", action="append", dest="str_outputs", type=str, default=[], help="Takes a string which represent the plaintext that will be encrypted with the given public key values")
cipher_parser.add_argument("--plaintext-file", "--pf", action="append", dest="input_files", type=Path, default=[], help="Path to a file wich represent the plaintext file that will be encrypted with the given public key values")
cipher_parser.add_argument("--plaintext-file-output", "--pfo", action="append", dest="file_outputs", type=path_or_stdout, default=[], help='TODO')
cipher_parser.add_argument("--standard", action="store", dest="padding", type=validate_padding, default="raw", help="Padding that will be used in the process for the given plaintext (--plaintext), choose one from the follows: [pkcs, oaep, raw] (default: raw)")
cipher_parser.add_argument("--json", "-j", action="store_true", dest="json", help="Make stdout outputs JSON")
cipher_parser.add_argument("--quiet", "--silent", "-s", action="store_true", dest="quiet", help='Suppress informative output')


uncipher_parser.add_argument("--key", action="store", dest="key", type=Path, default=None, help="Path to a private key file")
uncipher_parser.add_argument("-n", action="store", dest="n", type=parse_int_arg, default=None, help="<int> which specify RSA public modulus")
uncipher_parser.add_argument("-p", action="store", dest="p", type=parse_int_arg, default=None, help="<int> which specify RSA first prime factor")
uncipher_parser.add_argument("-q", action="store", dest="q", type=parse_int_arg, default=None, help="<int> which specify RSA second prime factor")
uncipher_parser.add_argument("-e", action="store", dest="e", type=parse_int_arg, default=None, help="<int> which specify RSA public exponent")
uncipher_parser.add_argument("-d", action="store", dest="d", type=parse_int_arg, default=None, help="<int> which specify RSA private exponent")
uncipher_parser.add_argument("-phi", "--phi", action="store", dest="phi", type=parse_int_arg, default=None, help="<int> which specify euler's phi of RSA public modulus")
uncipher_parser.add_argument("--ciphertext", "--ct", action="store", dest="inputs", type=parse_int_list, default=[], help="Takes an argument of <ciphertext> type which represent the ciphertext that will be encrypted with the given public key values")
uncipher_parser.add_argument("--ciphertext-output", "--co", action="append", dest="outputs", type=path_or_stdout, default=[], help='TODO')
uncipher_parser.add_argument("--ciphertext-string", "--cs", action="append", dest="input_strs", type=str, default=[], help="Takes a string which represent the ciphertext that will be encrypted with the given public key values")
uncipher_parser.add_argument("--ciphertext-string-output", "--cso", action="append", dest="str_outputs", type=str, default=[], help="Takes a string which represent the ciphertext that will be encrypted with the given public key values")
uncipher_parser.add_argument("--ciphertext-file", "--cf", action="append", dest="input_files", type=Path, default=[], help="Path to a file wich represent the ciphertext file that will be encrypted with the given public key values")
uncipher_parser.add_argument("--ciphertext-file-output", "--cfo", action="append", dest="file_outputs", type=path_or_stdout, default=[], help='TODO')
uncipher_parser.add_argument("--standard", action="store", dest="padding", type=validate_padding, default="raw", help="Padding that will be used in the process for the given ciphertext (--ciphertext), choose one from the follows: [pkcs, oaep, raw] (default: raw)")
uncipher_parser.add_argument("--json", "-j", action="store_true", dest="json", help="Make stdout outputs JSON")
uncipher_parser.add_argument("--quiet", "--silent", "-s", action="store_true", dest="quiet", help='Suppress informative output')


def _finalize_ciphertool_args(args, cipher=False):
    if cipher:
        if args.n is None and args.key is None:
            raise ValueError(f"Must specify either --key or -n")
        args.d, args.p, args.q, args.phi = None, None, None, None

    if args.key is not None and any(x is not None for x in (args.n, args.e, args.d, args.p, args.q, args.phi)):
        raise ValueError(f"--key and -n, -e... etc. cannot be specified at the same time")

    if args.key is not None:
        args.n, args.e, args.d, args.p, args.q = load_key(args.key)

    if not cipher:
        args.d = compute_d(args.n, args.e, args.d, args.p, args.q, args.phi)
        args.n = compute_n(args.n, args.e, args.d, args.p, args.q, args.phi)
        if args.n is None or args.d is None:
            raise ValueError(f"Not enough key elements to attemp decryption")

    if args.e is None:
        args.e = DEFAULT_E

    if not any((args.inputs, args.input_strs, args.input_files)):
        if cipher:
            raise ValueError(f"Must specify at least one of --plaintext, --plaintext-str or --plaintext-file")
        else:
            raise ValueError(f"Must specify at least one of --ciphertext, --ciphertext-str or --ciphertext-file")

    inputs = []
    for text in args.inputs:
        if args.outputs:
            inputs.append((text, args.outputs.pop(0)))
        else:
            inputs.append((text, True)) #stdout
    for text in args.input_strs:
        text = int.from_bytes(text.encode(), "big")
        if args.str_outputs:
            inputs.append((text, args.str_outputs.pop(0)))
        else:
            inputs.append((text, True)) #stdout
    for filename in args.input_files:
        with open(filename, "rb") as f:
            text = int.from_bytes(f.read(), "big")
        if args.file_outputs:
            inputs.append((text, args.file_outputs.pop(0)))
        else:
            inputs.append((text, filename.resolve().parent/filename.stem/".enc"))

    if any((args.outputs, args.str_outputs, args.file_outputs)):
        raise ValueError(f"Too many output specifications")

    args.inputs = inputs


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
pem_parser.add_argument("--json", "-j", action="store_true", dest="json", help="Make --dumpvalues output JSON")
pem_parser.add_argument("--quiet", "--silent", "-s", action="store_true", dest="quiet", help='Suppress informative output')


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
parser.add_argument("--isprime", action="store", dest="checkprime", type=parse_int_arg, default=None, help="Check if the given <int> is prime")
parser.add_argument("--eulerphi", action="store", dest="n_phi", type=parse_int_arg, default=None, help="<int> of which calc euler phi")
parser.add_argument("--show-attacks", action="store_true", dest="showattacks", help="Show implemented attacks")
parser.add_argument("--credits", action="store_true", dest="showcredits", help="Show credits")
parser.add_argument("--version", action="store_true", dest="showversion", help="Show version")
parser.add_argument("--quiet", "--silent", "-s", action="store_true", dest="quiet", help='Suppress informative output')


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
        "cipher": partial(_finalize_ciphertool_args, cipher=True),
        "uncipher": partial(_finalize_ciphertool_args, cipher=False),
        "pem": _finalize_pem_args,
        None: _finalize_general_args
    }

    args = parser.parse_args()
    finalize[args.csubp if args.subp == "ciphertool" else args.subp](args)

    return args
