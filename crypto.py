import sys
import binascii


from gmpy2 import invert

from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA

from pathlib import Path
from functools import partial

from utils import to_bytes_auto, DEFAULT_E


standards = {
    "oaep": PKCS1_OAEP,
    "pkcs": PKCS1_v1_5
}


def cipher(m, n, e=None, padding) -> int:
    """Encrypt a plaintext using RSA

    Arguments:
    m -- plaintext
    n -- RSA modulus
    e -- RSA public exponent
    padding -- padding type
    """

    if e is None:
        e = DEFAULT_E

    if m > n-2:
        e_mess = str(m)
        if len(e_mess) > 10:
            e_mess = f"{e_mess[:10]} ..."
        raise ValueError(f"Modulus to small for the given plaintext: {e_mess}")

    if padding == "raw":
        return pow(m, e, n)

    key = RSA.construct((n, e))
    standard = standards[padding]

    encryptor = standard.new(key)

    if standard is PKCS1_v1_5:
        encryptor.encrypt = partial(encryptor.encrypt, sentinel=None)

    return int.from_bytes(encryptor.encrypt(to_bytes_auto(m)), "big")


def uncipher(c, n, e=None, d, padding) -> int:
    """Decrypt a plaintext using RSA

    Arguments:
    c -- ciphertext
    n -- RSA modulus
    d -- RSA private exponent
    padding -- padding type
    """

    if e is None:
        e = DEFAULT_E

    c %= n

    if padding == "raw":
        return pow(c, d, n)

    key = RSA.construct((n, e, d))
    standard = standards[padding]

    decryptor = standard.new(key)

    if standard is PKCS1_v1_5:
        decryptor.decrypt = partial(decryptor.decrypt, sentinel=None)

    return int.from_bytes(decryptor.decrypt(to_bytes_auto(c)), "big")
