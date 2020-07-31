"""
Implement uncipher options
"""
import sys
import binascii

from os import system
from gmpy2 import invert

from Crypto.Util.Padding import unpad

from misc.hash_sum import *

"""
Decrypt a ciphertext string using RSA
"""
def rsa_uncipher_string(c: int, n: int, d: int, padding: str) -> tuple:
    
    print("[+] Decrypting ciphertext string\n")

    m = pow(c, d, n)

    if padding:
        print("[+] Unpad ciphertext with", padding, "\n")
        m_bytes = binascii.unhexlify(hex(m)[2:])
        m = int.from_bytes(unpad(m_bytes, len(m_bytes), style = padding), "big")
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
def rsa_uncipher_file(path_ciphertext: str, path_outfile: str, path_privkey: str, padding: str) -> None:
    
    print("[+] Decrypting ciphertext file\n")

    system("cipherfile-rsarmageddon " + "decrypt " + path_ciphertext + " " + path_outfile + " " + path_privkey + " " + padding)

    print("[+] original_file :", path_ciphertext, "-- sha256:", sha256_file_checksum(path_ciphertext))
    print("[+] decrypted_file:", path_outfile, "-- sha256:", sha256_file_checksum(path_outfile))
    print()