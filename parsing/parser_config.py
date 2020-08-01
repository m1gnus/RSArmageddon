import argparse

"""
Setting up the parser:
    argument parsing will be organized in different subparsers
    in order to improve readability and usability.
"""
parser = argparse.ArgumentParser(add_help = True)
subparser = parser.add_subparsers(dest = "subp")

"""
Attacks management
"""
attacks_parser = subparser.add_parser("attack", add_help = True)

attacks_parser.add_argument("-n", action = "store", dest = "n", type = str, default = None, help = "List of RSA public modules <int>,<int>,<int>...")
attacks_parser.add_argument("-e", action = "store", dest = "e", type = str, default = None, help = "List of RSA public exponents <int>,<int>,<int>...")
attacks_parser.add_argument("--n-e-file", action = "store", dest = "n_e_file", type = str, default = None, help = "Path to a file containing modules and public exponents, each lines is in the form \"n:e\" or \"n\"")
attacks_parser.add_argument("--timeout", action = "store", dest = "timeout", type = str, default = None, help = "Max elaboration time for attacks")
attacks_parser.add_argument("--attack", dest = "attacks", action = "store", default = None, help = "List of attacks that will be performed <str>,<str>,<str>,...")
attacks_parser.add_argument("--ext", action = "store", dest = "ext", type = str, default="pem", help = "Extension of public keys in the folder specified by --publickeydir")
attacks_parser.add_argument("--private", action = "store_const", dest = "private", const = True, default = False, help = "Dump private key file in PEM format if recovered")
attacks_parser.add_argument("--publickey", action = "store", dest = "publickey", type = str, default = None, help = "Path to a public key file")
attacks_parser.add_argument("--publickeydir", action = "store", dest = "publickey_dir", type = str, default = None, help = "Path to a folder containing public key files with extension ")
attacks_parser.add_argument("--uncipher", action = "store", dest = "ciphertext", type = str, default = None, help = "Ciphertext to decrypt if the private key is recovered")
attacks_parser.add_argument("--uncipher-file", action = "store", dest = "ciphertext_file", type = str, default = None, help = "File to uncipher if the private key is recovered")
attacks_parser.add_argument("--output-private", action = "store", dest = "output_private", type = str, default = None, help = "Specify where to save the private key file in PEM format if the private key is recovered and --private flag is setted")
attacks_parser.add_argument("--output-file", action = "store", dest = "output_file", type = str, default = "./decrypted.dec", help = "Specify where to save the decrypted file specified inn --uncipher-file if the private key is recovered (default: \"./decrypted.dec\")")
attacks_parser.add_argument("--output-dir", action = "store", dest = "output_dir", type = str, default = ".", help = "Specify where to save the private key files recovered from the public keys specified (for attacks which requires more than one public key couple of values (default: \".\")")

"""
Cipher tools
"""
tools_parser = subparser.add_parser("ciphertool", add_help = True)
csubparser = tools_parser.add_subparsers(dest = "csubp")

cipher_parser = csubparser.add_parser("cipher", add_help = True)
uncipher_parser = csubparser.add_parser("uncipher", add_help = True)

cipher_parser.add_argument("--key", action = "store", dest = "key", type = str, default = None, help = "Path to a public key file")
cipher_parser.add_argument("-n", action = "store", dest = "n", type = str, default = None, help = "<int> which specify RSA public modulus")
cipher_parser.add_argument("-e", action = "store", dest = "e", type = str, default = None, help = "<int> which specify RSA public exponent")
cipher_parser.add_argument("--plaintext", action = "store", dest = "plaintext", type = str, default = None, help = "Takes an argument of <plaintext> type which represent the plaintext that will be encrypted with the given public key values")
cipher_parser.add_argument("--plaintext-file", action = "store", dest = "plaintext_file", type = str, default = None, help = "Path to a file wich represent the plaintext file that will be encrypted with the given public key values")
cipher_parser.add_argument("--file-padding", action = "store", dest = "filepadding", type = str, default = "pkcs", help = "Padding that will be used in the process for the given file (--plaintext-file), choose one of the follows: [raw, pkcs, ssl, oaep, x931] (default: pkcs)")
cipher_parser.add_argument("--padding", action = "store", dest = "padding", type = str, default = None, help = "Padding that will be used in the process for the given plaintext (--plaintext), choose one from the follows: [pkcs7, iso7816, x923] (default: None)")
cipher_parser.add_argument("--output-file", action = "store", dest = "output_file", type = str, default = None, help = "Specify where to save the encrypted file (default: \"PLAINTEXT_FILE.enc\")")

uncipher_parser.add_argument("--key", action = "store", dest = "key", type = str, default = None, help = "Path to a private key file")
uncipher_parser.add_argument("-n", action = "store", dest = "n", type = str, default = None, help = "<int> which specify RSA public modulus")
uncipher_parser.add_argument("-p", action = "store", dest = "p", type = str, default = None, help = "<int> which specify RSA first prime factor")
uncipher_parser.add_argument("-q", action = "store", dest = "q", type = str, default = None, help = "<int> which specify RSA second prime factor")
uncipher_parser.add_argument("-e", action = "store", dest = "e", type = str, default = None, help = "<int> which specify RSA public exponent")
uncipher_parser.add_argument("-d", action = "store", dest = "d", type = str, default = None, help = "<int> which specify RSA private exponent")
uncipher_parser.add_argument("--ciphertext", action = "store", dest = "ciphertext", type = str, default = None, help = "Takes an argument of <ciphertext> type which represent the ciphertext that will be decrypted with the given private key values")
uncipher_parser.add_argument("--ciphertext-file", action = "store", dest = "ciphertext_file", type = str, default = None, help = "Path to a file wich represent the ciphertext file that will be decrypted with the given private key values")
uncipher_parser.add_argument("--file-padding", action = "store", dest = "filepadding", type = str, default = "pkcs", help = "Padding that will be used in the process for the given file (--ciphertext-file), choose one of the follows: [raw, pkcs, ssl, oaep, x931] (default: pkcs)")
uncipher_parser.add_argument("--padding", action = "store", dest = "padding", type = str, default = "", help = "Padding that will be used in the process for the given ciphertext (--ciphertext), choose one from the follows: [pkcs7, iso7816, x923] (default: None)")
uncipher_parser.add_argument("--output-file", action = "store", dest = "output_file", type = str, default = None, help = "Specify where to save the decrypted file (default: \"PLAINTEXT_FILE.dec\")")

"""
PEM manipulation
"""
pem_parser = subparser.add_parser("pem", add_help = True)

pem_parser.add_argument("--key", action = "store", dest = "key_path", type = str, default = None, help = "Path to a public/private key file")
pem_parser.add_argument("-n", action = "store", dest = "n", type = str, default = None, help = "<int> which specify RSA public modulus")
pem_parser.add_argument("-p", action = "store", dest = "p", type = str, default = None, help = "<int> which specify RSA first prime factor")
pem_parser.add_argument("-q", action = "store", dest = "q", type = str, default = None, help = "<int> which specify RSA second prime factor")
pem_parser.add_argument("-e", action = "store", dest = "e", type = str, default = None, help = "<int> which specify RSA public exponent")
pem_parser.add_argument("-d", action = "store", dest = "d", type = str, default = None, help = "<int> which specify RSA private exponent")
pem_parser.add_argument("--dumpvalues", action = "store_const", dest = "dumpvalues", const = True, default = False, help = "Dump numeric values from the given public/private key file (--key)")
pem_parser.add_argument("--createpub", action = "store_const", dest = "cpub", const = True, default = False, help = "Create a public key file in the specified format (--file-format) from numeric values")
pem_parser.add_argument("--createpriv", action = "store_const", dest = "cpriv", const = True, default = False, help = "Create a private key file in the specified format (--file-format) from numeric values")
pem_parser.add_argument("--generate", action = "store_const", dest = "generatekeypair", const = True, default = False, help = "Generate a new key pair")
pem_parser.add_argument("--file-format", action = "store", dest = "format", type = str, default = "PEM", help = "specify the key file format, choose one from the follows: [PEM, DER, OpenSSH] (default: PEM)")
pem_parser.add_argument("--output-priv", action = "store", dest = "opriv", type = str, default = None, help = "Specify where to save the private key file created with the given private key values if --createpriv flag is setted")
pem_parser.add_argument("--output-pub", action = "store", dest = "opub", type = str, default = None, help = "Specify where to save the public key file created with the given public key values if --createpub flag is setted")

"""
General features
"""
parser.add_argument("--factor", action = "store", dest = "tofactor", default = None, help = "<int> to factorize with pari's factor")
parser.add_argument("--ecm", action = "store", dest = "tofactorwecm", default = None, help = "<int> to factorize with ecm factorization")
parser.add_argument("--qs", action = "store", dest = "tofactorwqsieve", default = None, help = "<int> to factorize with quadratic sieve method")
parser.add_argument("--isprime", action = "store", dest = "checkprime", default = None, help = "Check if the given <int> is prime")
parser.add_argument("--show-attacks", action = "store_const", dest = "showattacks", const = True, default = False, help = "Show implemented attacks")
parser.add_argument("--credits", action = "store_const", dest = "showcredits", const = True,  default = False, help = "Show credits")
parser.add_argument("--version", action = "store_const", dest = "showversion", const = True,  default = False, help = "Show version")


"""
Initialize parser
"""
args = parser.parse_args()