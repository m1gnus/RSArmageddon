"""
Implement cipher options
"""
import sys
import binascii

from os import system
from gmpy2 import invert

from Crypto.Util.Padding import pad

from misc.hash_sum import *

"""
Encrypt a plaintext string using RSA
"""
def rsa_cipher_string(m: int, n: int, e: int, padding: str) -> tuple:
    
    if padding:
        print("[+] Pad plaintext with", padding)
        m_bytes = binascii.unhexlify(hex(m)[2:])
        m = int.from_bytes(pad(m_bytes, len(m_bytes), style = padding), "big")

    print("[+] Encrypting plaintext string\n")
    c = pow(m, e, n)
    hexc = hex(c) if (len(hex(c)) % 2) == 0 else ("0x0" + hex(c)[2:])
    rawc = binascii.unhexlify(hexc[2:].encode())
    print("[+] ciphertext (dec):", c)
    print("[+] ciphertext (hex):", hexc)
    print("[+] ciphertext (raw):", rawc)
    print()
    return (c, hexc, rawc)

"""
Encrypt a plaintext file using RSA
"""
def rsa_cipher_file(path_plaintext: str, path_outfile: str, path_pubkey: str, padding: str) -> None:
    
    print("[+] Encryptping plaintext file\n")

    system("cipher_tools/openssl_cipherfile.sh " + "encrypt " + path_plaintext + " " + path_outfile + " " + path_pubkey + " " + padding)

    print("[+] original_file :", path_plaintext, "-- sha256:", sha256_file_checksum(path_plaintext))
    print("[+] encrypted_file:", path_outfile, "-- sha256:", sha256_file_checksum(path_outfile))
    print()