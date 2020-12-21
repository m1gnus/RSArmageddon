import os
import sys

from pathlib import Path
from argparse import ArgumentParser, Action, Namespace, SUPPRESS

from certs import load_key
from parsing import (
        parse_int_arg,
        parse_time,
        parse_list,
        parse_std_list,
        path_or_stdout)


class ReadKeyFile(Action):
    def __call__(self, parser, namespace, path, option_string=None):
        key = load_key(path)
        for k, v in zip(("n", "e", "d", "p", "q"), key):
            if getattr(namespace, k, None) is None:
                setattr(namespace, k, v)


key_parser = ArgumentParser(add_help=False)
key_parser.add_argument("--key", "-k", action=ReadKeyFile, type=Path,          help="Path to a key file")
key_parser.add_argument("-n",          action="store",     type=parse_int_arg, help="RSA public modulus")
key_parser.add_argument("-e",          action="store",     type=parse_int_arg, help="RSA public exponent")
key_parser.add_argument("-d",          action="store",     type=parse_int_arg, help="RSA private exponent")
key_parser.add_argument("-p",          action="store",     type=parse_int_arg, help="RSA first prime factor")
key_parser.add_argument("-q",          action="store",     type=parse_int_arg, help="RSA second prime factor")
key_parser.add_argument("--phi",       action="store",     type=parse_int_arg, help="Euler's phi of RSA public modulus")


class Input(Action):
    def __call__(self, parser, namespace, input_, option_string=None):
        inputs = getattr(namespace, "inputs")
        inputs.append((input_, True))


class Output(Action):
    def __call__(self, parser, namespace, dest, option_string=None):
        inputs = getattr(namespace, "inputs", None)
        if not inputs:
            raise ValueError(f"{option_string} found but no inputs have been given yet") from e
        cur_text, _ = inputs[-1]
        inputs[-1] = (cur_text, dest)


text_parser_common = ArgumentParser(add_help=False)
text_parser_common.add_argument("--output", "-o", action=Output, type=path_or_stdout, help="")
text_parser_common.add_argument("--encryption-standard", "--std", action="store", type=parse_std_list, default=["pkcs"], help="")
text_parser_common.set_defaults(inputs=[])

plaintext_parser = ArgumentParser(add_help=False, parents=[text_parser_common])
plaintext_parser.add_argument("--plaintext",      "--pt",  "--encrypt",      action=Input, type=parse_int_arg, help="")
plaintext_parser.add_argument("--plaintext-raw",  "--ptr", "--encrypt-raw",  action=Input, type=os.fsencode,   help="")
plaintext_parser.add_argument("--plaintext-file", "--ptf", "--encrypt-file", action=Input, type=Path,          help="")

ciphertext_parser = ArgumentParser(add_help=False, parents=[text_parser_common])
ciphertext_parser.add_argument("--ciphertext",      "--ct",  "--decrypt",      action=Input, type=parse_int_arg, help="")
ciphertext_parser.add_argument("--ciphertext-raw",  "--ctr", "--decrypt-raw",  action=Input, type=os.fsencode,   help="")
ciphertext_parser.add_argument("--ciphertext-file", "--ctf", "--decrypt-file", action=Input, type=Path,          help="")
ciphertext_parser.add_argument("--encoding", action="store", help="")

commons_parser = ArgumentParser(argument_default=SUPPRESS, add_help=False)
commons_parser.add_argument("--show-attacks",            action="store_const", const=True, help="Show implemented attacks")
commons_parser.add_argument("--show-attacks-short",      action="store_const", const=True, help="Show implemented attacks")
commons_parser.add_argument("--show-encodings",          action="store_const", const=True, help="Show encodings")
commons_parser.add_argument("--credits",                 action="store_const", const=True, help="Show credits")
commons_parser.add_argument("--version",                 action="store_const", const=True, help="Show version")
commons_parser.add_argument("--json",                    action="store_const", const=True, help="Show version")
commons_parser.add_argument("--quiet", "--silent", "-s", action="store_const", const=True, help="Suppress informative output")
commons_parser.add_argument("--color", choices=["auto", "always", "never"], help="Suppress informative output")

main_parser = ArgumentParser(parents=[commons_parser])

scripts_parser = ArgumentParser(add_help=False)
scripts_parser.add_argument("n", action="store", type=parse_int_arg, help="")

command_subparsers = main_parser.add_subparsers(dest="command")
attack_parser = command_subparsers.add_parser("attack", parents=[commons_parser, ciphertext_parser])
pem_parser = command_subparsers.add_parser("pem", parents=[commons_parser, key_parser])
cipher_parser = command_subparsers.add_parser("encrypt", parents=[commons_parser, key_parser, plaintext_parser])
uncipher_parser = command_subparsers.add_parser("decrypt", parents=[commons_parser, key_parser, ciphertext_parser])
command_subparsers.add_parser("factor",   parents=[commons_parser, scripts_parser])
command_subparsers.add_parser("ecm",      parents=[commons_parser, scripts_parser])
command_subparsers.add_parser("isprime",  parents=[commons_parser, scripts_parser])
command_subparsers.add_parser("eulerphi", parents=[commons_parser, scripts_parser])

pem_parser.add_argument("--generate", "-g",                      action="store_true", help="")
pem_parser.add_argument("--dump-values", "--dumpvalues", "--dv", action="store_true", help="")
pem_parser.add_argument("--create-public", "--cpu",              action="store", type=path_or_stdout, help="")
pem_parser.add_argument("--create-private", "--cpr",             action="store", type=path_or_stdout, help="")
pem_parser.add_argument("--file-format", "--ff", choices=["pem", "der", "openssh"], default="pem", help="")


class NewKey(Action):
    def __call__(self, parser, namespace, n, option_string=None):
        keys = getattr(namespace, "keys")
        keys.append((n, None))


class SetE(Action):
    def __call__(self, parser, namespace, e, option_string=None):
        keys = getattr(namespace, "keys", None)
        if not keys:
            raise ValueError(f"-e found but no moduli (-n) have been given yet")
        n, _ = keys[-1]
        keys[-1] = (n, e)


attack_parser.add_argument("attacks", action="store", type=parse_list, help="")
attack_parser.add_argument("-n", action=NewKey, type=parse_int_arg, help="")
attack_parser.add_argument("-e", action=SetE, type=parse_int_arg, help="")
attack_parser.add_argument("--n-e-file", "--nef", action="append", dest="n_e_files", type=Path, default=[], help="")
attack_parser.add_argument("--timeout", "-t", action="store", type=parse_time, help="")
attack_parser.add_argument("--exts", "-x", action="store", type=parse_list, default=["pem", "pub"], help="")
attack_parser.add_argument("--output-key", "--ok", action="store_true", help="")
attack_parser.add_argument("--output-key-file", "--okf", action="store", type=path_or_stdout, help="")
attack_parser.add_argument("--output-key-dir", "--okd", action="store", type=Path, help="")
attack_parser.add_argument("--key", "-k", action="append", dest="key_paths", type=Path, default=[], help="")
attack_parser.add_argument("--recursive", "-r", action="store_true", help="")
attack_parser.set_defaults(keys=[])


class CustomNamespace(Namespace):
    def __init__(self):
        super().__init__()
        self.show_attacks=False
        self.show_attacks_short=False
        self.show_encodings=False
        self.credits=False
        self.version=False
        self.json=False
        self.quiet=False
        self.color="auto"


args = main_parser.parse_args(namespace=CustomNamespace())

if __name__ == "__main__":
    print(args)
