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
    try:
        keyfile = open(path, 'rb')
        key = RSA.importKey(keyfile.read())
    except Exception as e:
        print("certs_manipulation.py:dump_values_from_key ->", e)
    print("[+] Key imported\n")

    res = []

    print("[*] n: ", key.n)
    print("[*] e: ", key.e)

    res += [key.n, key.e]

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
    
    return res

"""
Takes n and e in order to create the corresponding formatted public key file in the specified format
"""
def create_pubkey(n: int, e: int, path: str) -> None:

    if not validate_modulous(n):
        sys.exit(1)
    
    file_format = input("file format? (PEM, DER, OpenSSH. Default: PEM) -> ")
    
    if file_format != 'PEM' and file_format != 'DER' and file_format != 'OpenSSH':
        print("[-] Unknown format... the key will be formatted in PEM format")
        file_format = 'PEM'

    key = RSA.construct((n, e)).exportKey(format = file_format)

    if path:
        print("[+] writing public key in", path)
        open(path, "wb").write(key)
    else:
        print("[-] no path specified, the key will be prompted to stdout\n")
        print(key.decode()) if file_format != 'DER' else print(key)