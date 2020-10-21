import sys
from pathlib import Path
from argparse import ArgumentParser, Action

from parsing import (
        parse_int_arg,
        parse_list,
        parse_int_list,
        validate_padding,
        validate_file_format,
        path_or_stdout)

from certs import load_key


class ReadKeyFile(Action):
    def __call__(self, parser, namespace, path, option_string=None):
        key = load_key(path)
        for k, v in zip(("n", "e", "d", "p", "q"), key):
            if getattr(namespace, k, None) is not None:
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
        inputs = getattr(namespace, "inputs", [])
        if not inputs:
            setattr(namespace, "inputs", inputs)
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
text_parser_common.add_argument("--encryption-standard", "--std", choices=["oaep", "pkcs", "raw"], help="")

plaintext_parser = ArgumentParser(add_help=False, parents=[text_parser_common])
plaintext_parser.add_argument("--plaintext",      "--pt",  "--encrypt",      action=Input, type=parse_int_arg, help="")
plaintext_parser.add_argument("--plaintext-raw",  "--ptr", "--encrypt-raw",  action=Input, type=str,           help="")
plaintext_parser.add_argument("--plaintext-file", "--ptf", "--encrypt-file", action=Input, type=Path,          help="")

ciphertext_parser = ArgumentParser(add_help=False, parents=[text_parser_common])
ciphertext_parser.add_argument("--ciphertext",      "--ct",  "--decrypt",      action=Input, type=parse_int_arg, help="")
ciphertext_parser.add_argument("--ciphertext-raw",  "--ctr", "--decrypt-raw",  action=Input, type=str,           help="")
ciphertext_parser.add_argument("--ciphertext-file", "--ctf", "--decrypt-file", action=Input, type=Path,          help="")

commons_parser = ArgumentParser(add_help=False)
commons_parser.add_argument("--show-attacks",            action="store_true", help="Show implemented attacks")
commons_parser.add_argument("--show-attacks-short",      action="store_true", help="Show implemented attacks")
commons_parser.add_argument("--credits",                 action="store_true", help="Show credits")
commons_parser.add_argument("--version",                 action="store_true", help="Show version")
commons_parser.add_argument("--json",                    action="store_true", help="Show version")
commons_parser.add_argument("--quiet", "--silent", "-s", action="store_true", help='Suppress informative output')

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

pem_parser.add_argument("--generate",       "-g",    action="store_true", help="")
pem_parser.add_argument("--dump-values",    "--dv",  action="store_true", help="")
pem_parser.add_argument("--create-public",  "--cpu", action="store", type=path_or_stdout, help="")
pem_parser.add_argument("--create-private", "--cpr", action="store", type=path_or_stdout, help="")
pem_parser.add_argument("--file-format",    "--ff",  choices=["pem", "der", "openssh"], default="pem", help="")


class NewKey(Action):
    def __call__(self, parser, namespace, n, option_string=None):
        keys = getattr(namespace, "keys", [])
        if not keys:
            setattr(namespace, "keys", keys)
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
attack_parser.add_argument("--n-e-file", "--nef", action="append", dest="nefs", type=Path, default=[], help="")
attack_parser.add_argument("--key", "-k", action="append", dest="key_files", type=Path, default=[], help="")
attack_parser.add_argument("--key-dir", "--kd", action="append", dest="key_dirs", type=Path, default=[], help="")
attack_parser.add_argument("--timeout", "-t", action="store", type=int, help="")
attack_parser.add_argument("--exts", "-x", action="store", type=parse_list, default=["pem", "pub"], help="")
attack_parser.add_argument("--output-key", "--ok", action="store_true", help="")
attack_parser.add_argument("--output-key-file", "--okf", action="store", type=path_or_stdout, help="")
attack_parser.add_argument("--output-key-dir", "--okd", action="store", type=Path, help="")


args = main_parser.parse_args()
