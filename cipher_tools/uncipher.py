"""
Implement uncipher options
"""
import sys
import binascii

from os import system
from gmpy2 import invert

from misc.hash_sum import *

"""
Decrypt a ciphertext string using RSA
"""
def rsa_uncipher_string(c: int, n: int, d: int) -> tuple:
    
    print("[+] Decrypting ciphertext string\n")
    m = pow(c, d, n)
    hexm = hex(m) if (len(hex(m)) % 2) == 0 else ("0x0" + hex(m)[2:])
    rawm = binascii.unhexlify(hexm[2:].encode())
    print("[+] ciphertext (dec):", m)
    print("[+] ciphertext (hex):", hexm)
    print("[+] ciphertext (raw):", rawm)
    print()
    return (m, hexm, rawm)

"""
Decrypt a ciphertext file using RSA
"""
def rsa_uncipher_file(path_ciphertext: str, path_outfile: str, path_privkey: str) -> None:
    
    print("[+] Decrypting ciphertext file\n")

    system("cipher_tools/openssl_cipherfile.sh " + "decrypt " + path_ciphertext + " " + path_outfile + " " + path_privkey)

    print("[+] original_file :", path_ciphertext, "-- sha256:", sha256_file_checksum(path_ciphertext))
    print("[+] decrypted_file:", path_outfile, "-- sha256:", sha256_file_checksum(path_outfile))
    print()