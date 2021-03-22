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

import sys
import binascii

from pathlib import Path
from functools import partial
from gmpy2 import invert
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA

from .utils import to_bytes_auto, DEFAULT_E


standards = {
    "oaep": PKCS1_OAEP,
    "pkcs": PKCS1_v1_5
}


def cipher(m, n, e=None, std="pkcs"):
    """Encrypt a plaintext using RSA

    Arguments:
    m -- plaintext
    n -- RSA modulus
    e -- RSA public exponent
    std -- encryption standard
    """

    if e is None:
        e = DEFAULT_E

    if m > n-2:
        e_mess = str(m)
        if len(e_mess) > 10:
            e_mess = f"{e_mess[:10]} ..."
        raise ValueError(f"Modulus too small for plaintext: {e_mess}")

    if std == "raw":
        return pow(m, e, n)

    key = RSA.construct((n, e))
    standard = standards[std]

    encryptor = standard.new(key)

    return int.from_bytes(encryptor.encrypt(to_bytes_auto(m)), "big")


def uncipher(c, n, e=None, d=None, std="pkcs"):
    """Decrypt a plaintext using RSA

    Arguments:
    c -- ciphertext
    n -- RSA modulus
    d -- RSA private exponent
    std -- encryption standard
    """

    if e is None:
        e = DEFAULT_E

    c %= n

    if std == "raw":
        return pow(c, d, n)

    key = RSA.construct((n, e, d))
    standard = standards[std]

    decryptor = standard.new(key)

    if standard is PKCS1_v1_5:
        decryptor.decrypt = partial(decryptor.decrypt, sentinel=None)

    dec = decryptor.decrypt(to_bytes_auto(c))
    if dec is None:
        raise ValueError(f"Invalid ciphertext (encryption standard: {std})")
    return int.from_bytes(dec, "big")
