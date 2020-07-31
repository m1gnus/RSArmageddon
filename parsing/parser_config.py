import argparse

"""
Setting up the parser:
    argument parsing will be organized in different subparsers
    in order to improve readability and usability.
"""
parser = argparse.ArgumentParser(add_help = True)
subparser = parser.add_subparsers(dest = 'subp')

"""
Attacks management
"""
attacks_parser = subparser.add_parser('attack', add_help = True)

attacks_parser.add_argument('--publickey', action = 'store', dest = 'publickey', type = str, default = None, help = "Path to a public key in PEM format")
attacks_parser.add_argument('--publickeydir', action = 'store', dest = 'publickey_dir', type = str, default = None, help = 'Path to a folder containing public keys in PEM format')
attacks_parser.add_argument('--attack', dest = 'attacks', action = 'store', default = None, help = 'attack1,attack2,attack3.......')
attacks_parser.add_argument('-n', action = 'store', dest = 'n', type = str, default = None)
attacks_parser.add_argument('-e', action = 'store', dest = 'e', type = str, default = None)
attacks_parser.add_argument('--n_e_file', action = 'store', dest = 'n_e_file', type = str, default = None, help = 'Path to a file containing modulusses and public exponents')
attacks_parser.add_argument('--ext', action = 'store', dest = 'ext', type = str, default="pem", help = 'Extension of public keys in folder')
attacks_parser.add_argument('--private', action = 'store_const', dest = 'private', const = False, default = True, help = "Dump private key im PEM format if recovered")
attacks_parser.add_argument('--uncipher', action = 'store', dest = 'ciphertext', type = str, default = None, help = "Ciphertext to decrypt")
attacks_parser.add_argument('--uncipher-file', action = 'store', dest = 'ciphertext_file', type = str, default = None, help = 'Uncipher this file if attack succeded')
attacks_parser.add_argument('--output-private', action = 'store', dest = 'output_private', type = str, default = None, help = 'Path to private key file')
attacks_parser.add_argument('--output-file', action = 'store', dest = 'output_file', type = str, default = "./decrypted.dec", help = 'Path to decrypted file')
attacks_parser.add_argument('--output-dir', action = 'store', dest = 'output_dir', type = str, default = ".", help = 'Path to decrypted files folder')
attacks_parser.add_argument('--timeout', action = 'store', dest = 'timeout', type = str, default = None, help = "max elaboration time for attacks")

"""
Cipher tools
"""
tools_parser = subparser.add_parser('ciphertool', add_help = True)
csubparser = tools_parser.add_subparsers(dest = 'csubp')

cipher_parser = csubparser.add_parser('cipher', add_help = True)
uncipher_parser = csubparser.add_parser('uncipher', add_help = True)

cipher_parser.add_argument('--key', action = 'store', dest = 'key', type = str, default = None, help = 'Path to a public key in PEM format')
cipher_parser.add_argument('-n', action = 'store', dest = 'n', type = str, default = None)
cipher_parser.add_argument('-e', action = 'store', dest = 'e', type = str, default = None)
cipher_parser.add_argument('--file-padding', action = 'store', dest = 'filepadding', type = str, default = "pkcs", help = "raw, pkcs, ssl, oaep")
cipher_parser.add_argument('--padding', action = 'store', dest = 'padding', type = str, default = '', help = "pkcs7, iso7816, x923")
cipher_parser.add_argument('--plaintext', action = 'store', dest = 'plaintext', type = str, default = None)
cipher_parser.add_argument('--plaintext-file', action = 'store', dest = 'plaintext_file', type = str, default = None, help = "Path to a file to encrypt")
cipher_parser.add_argument('--output-file', action = 'store', dest = 'output_file', type = str, default = None, help = 'Path to encrypted file')

uncipher_parser.add_argument('--key', action = 'store', dest = 'key', type = str, default = None, help = 'Path to a private key in PEM format')
uncipher_parser.add_argument('-n', action = 'store', dest = 'n', type = str, default = None)
uncipher_parser.add_argument('-p', action = 'store', dest = 'p', type = str, default = None)
uncipher_parser.add_argument('-q', action = 'store', dest = 'q', type = str, default = None)
uncipher_parser.add_argument('-e', action = 'store', dest = 'e', type = str, default = None)
uncipher_parser.add_argument('-d', action = 'store', dest = 'd', type = str, default = None)
uncipher_parser.add_argument('--file-padding', action = 'store', dest = 'filepadding', type = str, default = "pkcs", help = "raw, pkcs, ssl, oaep, x931")
uncipher_parser.add_argument('--padding', action = 'store', dest = 'padding', type = str, default = '', help = "pkcs7, iso7816, x923")
uncipher_parser.add_argument('--ciphertext', action = 'store', dest = 'ciphertext', type = str, default = None)
uncipher_parser.add_argument('--ciphertext-file', action = 'store', dest = 'ciphertext_file', type = str, default = None, help = "Path to a file to decrypt")
uncipher_parser.add_argument('--output-file', action = 'store', dest = 'output_file', type = str, default = None, help = 'Path to decrypted file')

"""
PEM manipulation
"""
pem_parser = subparser.add_parser('pem', add_help = True)

pem_parser.add_argument('--key', action = 'store', dest = 'key_path', type = str, default = None, help = 'Path to a key in PEM format')
pem_parser.add_argument('-n', action = 'store', dest = 'n', type = str, default = None)
pem_parser.add_argument('-p', action = 'store', dest = 'p', type = str, default = None)
pem_parser.add_argument('-q', action = 'store', dest = 'q', type = str, default = None)
pem_parser.add_argument('-e', action = 'store', dest = 'e', type = str, default = None)
pem_parser.add_argument('-d', action = 'store', dest = 'd', type = str, default = None)
pem_parser.add_argument('--output-priv', action = 'store', dest = 'opriv', type = str, default = None)
pem_parser.add_argument('--output-pub', action = 'store', dest = 'opub', type = str, default = None)
pem_parser.add_argument('--file-format', action = 'store', dest = 'format', type = str, default = 'PEM', help = "file format? (PEM, DER, OpenSSH. Default: PEM)")
pem_parser.add_argument('--dumpvalues', action = 'store_const', dest = 'dumpvalues', const = True, default = False, help = 'Dump numeric values from a key in PEM format')
pem_parser.add_argument('--createpub', action = 'store_const', dest = 'cpub', const = True, default = False, help = 'Create a public key file in PEM format from numeric values')
pem_parser.add_argument('--createpriv', action = 'store_const', dest = 'cpriv', const = True, default = False, help = 'Create a private key file in PEM format from numeric values')
pem_parser.add_argument('--generate', action = 'store_const', dest = 'generatekeypair', const = True, default = False, help = 'Create a new key pair')

"""
General options
"""
parser.add_argument('--factor', action = 'store', dest = 'tofactor', default = None, help = 'Integer to factorize')
parser.add_argument('--ecm', action = 'store', dest = 'tofactorwecm', default = None, help = 'Integer to factorize with ecm')
parser.add_argument('--qsieve', action = 'store', dest = 'tofactorwqsieve', default = None, help = 'Integer to factorize with quadratic sieve method')
parser.add_argument('--isprime', action = 'store', dest = 'checkprime', default = None, help = 'Check if the given integer is prime')
parser.add_argument('--show-attacks', action = 'store_const', dest = 'showattacks', const = True, default = False, help = 'show implemented attacks')
parser.add_argument('--credits', action = 'store_const', dest = 'showcredits', const = True,  default = False, help = 'show credits')
parser.add_argument('--version', action = 'store_const', dest = 'showversion', const = True,  default = False, help = 'show version')


"""
Initialize parser
"""
args = parser.parse_args()