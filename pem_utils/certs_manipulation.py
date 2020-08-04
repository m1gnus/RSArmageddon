"""
Implement --dumpvalues --createpriv --createpub --generate
"""

import sys

from gmpy2 import invert 
from Crypto.PublicKey import RSA

from parsing.args_filter import *

"""
Takes a path to a public/private key and dumps its values using pycryptodome RSA methods
the values will also be returned in a list: [n, e[, p, q, d, dp, dq, pinv, qinv]]
"""
def dump_values_from_key(path: str) -> list:

    print("[+] Importing Key")

    """
    obtain a RsaKey object from the key file: https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html 
    """
    try:
        keyfile = open(path, "rb")
        key = RSA.importKey(keyfile.read())
    except Exception as e:
        print("certs_manipulation.py:dump_values_from_key ->", e)
        sys.exit(1)

    print("[+] Key imported\n")

    res = []

    print("[*] n: ", key.n)
    print("[*] e: ", key.e)

    res += [key.n, key.e]

    """
    If the key is a private key dump the private key values
    """
    if key.has_private():
        print("[*] p: ", key.p)
        print("[*] q: ", key.q)
        print("[*] d: ", key.d)
        print()

        dp = key.d%(key.p-1)
        dq = key.d%(key.q-1)
        pinv = int(invert(key.p, key.q))
        qinv = int(invert(key.q, key.p))

        print("[#] dp: ", dp)
        print("[#] dq: ", dq)
        print("[#] pinv: ", pinv)
        print("[#] qinv: ", qinv)

        res += [key.p, key.q, key.d, dp, dq, pinv, qinv]
    
    print()
    
    return res

"""
Takes n and e in order to create the corresponding public key file formatted in the specified format
"""
def create_pubkey(n: int, e: int, path: str, file_format: str) -> None:

    if not validate_modulus(n):
        sys.exit(1)

    """
    make sure that file_format is a valid format
    """
    valid_format = ["PEM", "DER", "OpenSSH"]
    if file_format not in valid_format:
        print("[-] Unknown format... the key will be formatted in PEM format")
        file_format = "PEM"

    """
    build the key in the specified format
    """
    key = RSA.construct((n, e)).exportKey(format = file_format)

    if path:
        print("[+] writing public key in", path)
        open(path, "wb").write(key)
    else:
        print("[-] no path specified, the key will be prompted to stdout\n")
        print(key.decode() + "\n") if file_format != "DER" else print(key, "\n")

"""
Takes n,e,d,p and q in order to create the corresponding private key file formatted in the specified format
"""
def create_privkey(n: int, e: int, d: int, p: int, q: int, path: str, file_format: str) -> None:

    """
    recover all the arguments from the given ones.

    fill_privkey_args() will check if the the given arguments are sufficient in order to create a private key
    and if the provided arguments are consistent
    """
    n, e, d, p, q = fill_privkey_args(n, e, d, p, q)
    
    """
    make sure that file_format is a valid format
    """
    valid_format = ["PEM", "DER", "OpenSSH"]
    if file_format not in valid_format:
        print("[-] Unknown format... the key will be formatted in PEM format")
        file_format = "PEM"
    
    """
    build the key in the specified format
    """
    key = RSA.construct((n, e, d, p, q)).exportKey(format = file_format)

    if path and path != "None":
        print("[+] writing private key in", path)
        open(path, "wb").write(key)
    else:
        print("[-] no path specified, the key will be prompted to stdout\n")
        print(key.decode() + "\n") if file_format != "DER" else print(key, "\n")

"""
Generate a new keypair
"""
def generate_keypair(e: int, pubpath: str, privpath: str) -> None:
    
    """
    generate the key
    """
    key = RSA.generate(2048, e=e)

    """
    obtain public and private key
    """
    privkey = key.exportKey()
    pubkey = key.publickey().exportKey()

    if pubpath:
        print("[+] writing public key in", pubpath)
        open(pubpath, "wb").write(pubkey)
    else:
        print("[-] no path specified, the public key will be prompted to stdout\n")
        print(pubkey.decode() + "\n")

    if privpath:
        print("[+] writing private key in", privpath)
        open(privpath, "wb").write(privkey)
    else:
        print("[-] no path specified, the private key will be prompted to stdout\n")
        print(privkey.decode() + "\n")
