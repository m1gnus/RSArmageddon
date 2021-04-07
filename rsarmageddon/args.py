##########################################################################
# RSArmageddon - RSA cryptography and cryptoanalysis toolkit             #
# Copyright (C) 2020,2021                                                #
# Vittorio Mignini a.k.a. M1gnus <vittorio.mignini@gmail.com>            #
# Simone Cimarelli a.k.a. Aquilairreale <aquilairreale@ymail.com>        #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

import os
import sys

from textwrap import dedent
from functools import partial
from pathlib import Path
from argparse import ArgumentParser, Action, Namespace, SUPPRESS, RawDescriptionHelpFormatter

from .certs import load_key
from .parsing import (
        parse_int_arg,
        parse_time,
        parse_list,
        parse_std_list,
        path_or_stdout)


help_formatter = partial(RawDescriptionHelpFormatter, max_help_position=30)

main_description = dedent("""\
        RSArmageddon: Smashing RSA for fun and profit

        Commands:
          attack                      execute attacks
          pem                         manage keys and key files
          encrypt                     encrypt data and files
          decrypt                     decrypt data and files
          factor                      factorize a number with PARI factorization
          ecm                         factorize a number with ellyptic curve method
          isprime                     primality test
          eulerphi                    calculate euler phi of a number""")

attack_description = dedent("""\
        Attack weak public keys and recover private keys""")

pem_description = dedent("""\
        Manage keys and key files""")

cipher_description = dedent("""\
        Encrypt data and files using different encryption standards""")

uncipher_description = dedent("""\
        Decrypt data and files using different encryption standards""")

factor_description = dedent("""\
        Factorize a number using PARI factorization""")

ecm_description = dedent("""\
        Factorize a number using elliptic curve method""")

isprime_description = dedent("""\
        Primality test""")

eulerphi_description = dedent("""\
        Calculate Euler's phi function of a number""")

epilog = dedent("""\
        Number format:
            All numbers can be input in a variety of formats and bases.
            RSArmageddon understands regular base 10 numbers and python literals
            introduced by 0x for hex, 0o for octal or 0b for binary.
            Other less common bases can be specified in the form number:base
            where base is either an integer between 2 and 32, b64 for base64, or
            b85 for base85""")


class ReadKeyFile(Action):
    def __call__(self, parser, namespace, path, option_string=None):
        key = load_key(path)
        for k, v in zip(("n", "e", "d", "p", "q"), key):
            if getattr(namespace, k, None) is None:
                setattr(namespace, k, v)


key_parser = ArgumentParser(add_help=False)
key_parser.add_argument("--key", "-k", action=ReadKeyFile, type=Path,          metavar="FILE",   help="Path to a key file")
key_parser.add_argument("-n",          action="store",     type=parse_int_arg, metavar="NUMBER", help="RSA public modulus")
key_parser.add_argument("-e",          action="store",     type=parse_int_arg, metavar="NUMBER", help="RSA public exponent")
key_parser.add_argument("-d",          action="store",     type=parse_int_arg, metavar="NUMBER", help="RSA private exponent")
key_parser.add_argument("-p",          action="store",     type=parse_int_arg, metavar="NUMBER", help="RSA first prime factor")
key_parser.add_argument("-q",          action="store",     type=parse_int_arg, metavar="NUMBER", help="RSA second prime factor")
key_parser.add_argument("--phi",       action="store",     type=parse_int_arg, metavar="NUMBER", help="Euler's phi of RSA public modulus")

format_parser = ArgumentParser(add_help=False)
format_parser.add_argument("--file-format", "--ff", choices=["pem", "der", "openssh", "json"], default="pem", help="Set output key file format")


class Input(Action):
    def __call__(self, parser, namespace, input_, option_string=None):
        namespace.inputs.append((input_, True))


class Output(Action):
    def __call__(self, parser, namespace, dest, option_string=None):
        if not namespace.inputs:
            raise ValueError(f"{option_string} found but no inputs have been given yet") from e
        cur_text, _ = namespace.inputs.pop()
        namespace.inputs.append((cur_text, dest))


text_parser_common = ArgumentParser(add_help=False)
text_parser_common.add_argument("--encryption-standard", "--std", action="store", type=parse_std_list, default=["pkcs"], metavar="STD", help="Comma-separated list. Try to use these encryption standards when reading or writing ciphertext files (default: pkcs)")
text_parser_common.set_defaults(inputs=[])

plaintext_parser = ArgumentParser(add_help=False, parents=[text_parser_common])
plaintext_parser.add_argument("--plaintext",      "--pt",  "--encrypt",      action=Input,  type=parse_int_arg,  metavar="NUMBER",        help="Use number as plaintext")
plaintext_parser.add_argument("--plaintext-raw",  "--ptr", "--encrypt-raw",  action=Input,  type=os.fsencode,    metavar="BINARY_STRING", help="Use string as plaintext")
plaintext_parser.add_argument("--plaintext-file", "--ptf", "--encrypt-file", action=Input,  type=Path,           metavar="FILE",          help="Use file as plaintext")
plaintext_parser.add_argument("--output",         "-o",                      action=Output, type=path_or_stdout, metavar="FILE",          help="Output ciphertext to file or stdout (applies to previous input)")

ciphertext_parser = ArgumentParser(add_help=False, parents=[text_parser_common])
ciphertext_parser.add_argument("--encoding", action="store", help="")
ciphertext_parser.add_argument("--ciphertext",      "--ct",  "--decrypt",      action=Input,  type=parse_int_arg,  metavar="NUMBER",        help="Use number as ciphertext")
ciphertext_parser.add_argument("--ciphertext-raw",  "--ctr", "--decrypt-raw",  action=Input,  type=os.fsencode,    metavar="BINARY_STRING", help="Use string as ciphertext")
ciphertext_parser.add_argument("--ciphertext-file", "--ctf", "--decrypt-file", action=Input,  type=Path,           metavar="FILE",          help="Use file as ciphertext")
ciphertext_parser.add_argument("--output",          "-o",                      action=Output, type=path_or_stdout, metavar="FILE",          help="Output plaintext to file or stdout (applies to previous input)")

commons_parser = ArgumentParser(argument_default=SUPPRESS, add_help=False)
commons_parser.add_argument("--show-attacks",            action="store_const", const=True, help="Show all available attacks")
commons_parser.add_argument("--show-attacks-short",      action="store_const", const=True, help="Show all available attacks (short form)")
commons_parser.add_argument("--show-encodings",          action="store_const", const=True, help="Show all available encodings")
commons_parser.add_argument("--credits",                 action="store_const", const=True, help="Show credits")
commons_parser.add_argument("--version", "-V",           action="store_const", const=True, help="Show version")
commons_parser.add_argument("--json",                    action="store_const", const=True, help="Turn on json output format")
commons_parser.add_argument("--quiet", "--silent", "-s", action="store_const", const=True, help="Suppress informative output")
commons_parser.add_argument("--color",                choices=["auto", "always", "never"], help="Set color output behavior")

main_parser = ArgumentParser(parents=[commons_parser], formatter_class=help_formatter, description=main_description)

scripts_parser = ArgumentParser(add_help=False)
scripts_parser.add_argument("n", action="store", type=parse_int_arg, metavar="NUMBER", help="Input number")

command_subparsers = main_parser.add_subparsers(dest="command")
attack_parser   = command_subparsers.add_parser("attack",  parents=[commons_parser, format_parser, ciphertext_parser], formatter_class=help_formatter, description=attack_description,   epilog=epilog)
pem_parser      = command_subparsers.add_parser("pem",     parents=[commons_parser, format_parser, key_parser],        formatter_class=help_formatter, description=pem_description,      epilog=epilog)
cipher_parser   = command_subparsers.add_parser("encrypt", parents=[commons_parser, key_parser, plaintext_parser],     formatter_class=help_formatter, description=cipher_description,   epilog=epilog)
uncipher_parser = command_subparsers.add_parser("decrypt", parents=[commons_parser, key_parser, ciphertext_parser],    formatter_class=help_formatter, description=uncipher_description, epilog=epilog)
command_subparsers.add_parser("factor",                    parents=[commons_parser, scripts_parser],                   formatter_class=help_formatter, description=factor_description,   epilog=epilog)
command_subparsers.add_parser("ecm",                       parents=[commons_parser, scripts_parser],                   formatter_class=help_formatter, description=ecm_description,      epilog=epilog)
command_subparsers.add_parser("isprime",                   parents=[commons_parser, scripts_parser],                   formatter_class=help_formatter, description=isprime_description,  epilog=epilog)
command_subparsers.add_parser("eulerphi",                  parents=[commons_parser, scripts_parser],                   formatter_class=help_formatter, description=eulerphi_description, epilog=epilog)

pem_parser.add_argument("--generate", "-g",                      action="store_true",                                      help="Generate a new 2048 bit key pair")
pem_parser.add_argument("--dump-values", "--dumpvalues", "--dv", action="store_true",                                      help="Dump key values to standard output")
pem_parser.add_argument("--create-public", "--cpu",              action="store", type=path_or_stdout, metavar="FILE",      help="Output public key to file")
pem_parser.add_argument("--create-private", "--cpr",             action="store", type=path_or_stdout, metavar="FILE",      help="Output private key to file")


class NewKey(Action):
    def __call__(self, parser, namespace, n, option_string=None):
        namespace.keys.append((n, None))


class SetE(Action):
    def __call__(self, parser, namespace, e, option_string=None):
        if not namespace.keys:
            raise ValueError(f"-e found but no moduli (-n) have been given yet")
        n, _ = namespace.keys.pop()
        namespace.keys.append((n, e))


attack_parser.add_argument("attacks",                    action="store",                                type=parse_list,     metavar="ATTACKS_LIST", help="Comma-separated list of attacks to be executed")
attack_parser.add_argument("-n",                         action=NewKey,                                 type=parse_int_arg,  metavar="NUMBER",       help="Target key RSA public modulus")
attack_parser.add_argument("-e",                         action=SetE,                                   type=parse_int_arg,  metavar="NUMBER",       help="Target key RSA public exponent (applies to preceding -n)")
attack_parser.add_argument("--n-e-file", "--nef",        action="append", dest="n_e_files", default=[], type=Path,           metavar="FILE",         help="Read target public keys from text FILE, one comma-separated n,e pair per line")
attack_parser.add_argument("--key", "-k",                action="append", dest="key_paths", default=[], type=Path,           metavar="PATH",         help="Read target public keys from PATH. PATH can either be a single key file or a directory containing key files")
attack_parser.add_argument("--exts", "-x",               action="store",  default=["pem", "pub"],       type=parse_list,     metavar="EXTENSIONS",   help="Comma-separated list of file extensions. Selects which files are picked up by -k when PATH is a directory")
attack_parser.add_argument("--recursive", "-r",          action="store_true",                                                                        help="Descend recursively inside directories when looking for key files (-k only looks into the first level by default)")
attack_parser.add_argument("--output-key", "--ok",       action="store_true",                                                                        help="Output first cracked key to standard output")
attack_parser.add_argument("--output-key-file", "--okf", action="store",                                type=path_or_stdout, metavar="FILE",         help="Output first cracked key to FILE")
attack_parser.add_argument("--output-key-dir", "--okd",  action="store",                                type=Path,           metavar="DIRECTORY",    help="Output all cracked keys to this directory")
attack_parser.add_argument("--timeout", "-t",            action="store",                                type=parse_time,     metavar="TIME",         help="Set maximum run time allowed for each attack")
attack_parser.set_defaults(keys=[])


class RSArmageddonNamespace(Namespace):
    def __init__(self):
        super().__init__()
        self.key = []
        self.n = None
        self.e = None
        self.d = None
        self.p = None
        self.q = None
        self.phi = None
        self.encryption_standard = ["pkcs"]
        self.plaintext = None
        self.plaintext_raw = None
        self.plaintext_file = None
        self.output = None
        self.encoding = None
        self.ciphertext = None
        self.ciphertext_raw = None
        self.ciphertext_file = None
        self.show_attacks = False
        self.show_attacks_short = False
        self.show_encodings = False
        self.credits = False
        self.version = False
        self.json = False
        self.quiet = False
        self.color = "auto"
        self.generate = False
        self.dump_values = False
        self.create_public = None
        self.create_private = None
        self.file_format = "pem"
        self.attacks = None
        self.n_e_file = []
        self.exts = ["pem", "pub"]
        self.recursive = False
        self.output_key = False
        self.output_key_file = None
        self.output_key_dir = None
        self.timeout = None
        self.inputs=[]
        self.keys=[]

    def parse(self):
        main_parser.parse_args(namespace=self)


args = RSArmageddonNamespace()


if __name__ == "__main__":
    parse()
    print(args)
