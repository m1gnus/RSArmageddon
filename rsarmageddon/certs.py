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
import json

from contextlib import redirect_stdout
from pathlib import Path

from gmpy2 import invert
from Crypto.PublicKey import RSA

from .utils import output, DEFAULT_E


common_formats = {
    ".pem": "PEM",
    ".der": "DER",
    ".openssh": "OpenSSH"
}


private_formats = {}
private_formats.update(common_formats)

public_formats = {".pub": "PEM"}
public_formats.update(common_formats)


def infer_format_priv(p):
    """Infer private key file format from extension

    Arguments:
    p -- path to key file
    """
    try:
        return private_formats[p.suffix] if isinstance(p, Path) else None
    except KeyError:
        return None


def infer_format_pub(p):
    """Infer public key file format from extension

    Arguments:
    p -- path to key file
    """
    try:
        return public_formats[p.suffix] if isinstance(p, Path) else None
    except KeyError:
        return None


def generate_key(e=None):
    """Generate a new key randomly

    Keyword Arguments:
    e -- RSA public exponent
    """
    e = e if e is not None else DEFAULT_E
    key = RSA.generate(2048, e=e)
    return key.n, key.e, key.d, key.p, key.q


def print_key(n=None, e=None, d=None, p=None, q=None, dp=None, dq=None, pinv=None, qinv=None):
    """Print key elements in a more readable format

    Keyword arguments:
    n -- RSA public modulus
    e -- RSA public exponent
    d -- RSA private exponent
    p -- first factor
    q -- second factor
    dp
    dq
    pinv
    qinv
    file -- file-like object
    """
    output.primary(f"n: {n}")
    output.primary(f"e: {e}")
    output.primary(f"d: {d}")
    output.primary(f"p: {p}")
    output.primary(f"q: {q}")
    output.newline()
    output.secondary(f"dp: {dp}")
    output.secondary(f"dq: {dq}")
    output.secondary(f"pinv: {pinv}")
    output.secondary(f"qinv: {qinv}")
    output.newline()


def print_key_json(n=None, e=None, d=None, p=None, q=None, dp=None, dq=None, pinv=None, qinv=None):
    d = {k: str(v) for k, v in locals().items()}
    json.dump(d, sys.stdout, indent=4)
    print()


def load_key(path):
    """Load key elements from a key file

    Arguments:
    path -- path to a key file
    """

    # obtain a RsaKey object from the key file: https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html 
    keyfile = open(path, "rb")
    key = RSA.importKey(keyfile.read())

    # If the key is a private key dump the private key values
    if key.has_private():
        return key.n, key.e, key.d, key.p, key.q
    else:
        return key.n, key.e, None, None, None


def load_keys(path, exts=("pem", "pub"), recursive=False):
    """Load key elements from keys found in a directory

    Arguments:
    path -- path to keys directory
    exts -- iterable of file extensions
    """
    keys = []
    path = Path(path)

    for ext in exts:
        if not ext.startswith("."):
            ext = f".{ext}"

        pattern = f"*{ext}"
        if recursive:
            pattern = f"**/{pattern}"

        for key_file in path.glob(pattern):
            n, e, _, _, _ = load_key(key_file)
            keys.append(((n, e), key_file.stem))

    return keys


file_formats = {
    "pem": "PEM",
    "der": "DER",
    "openssh": "OpenSSH",
    "json": "JSON"
}


def encode_pubkey(n, e, file_format):
    """Encode a public key to file_format

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    file_format -- file format
    """
    file_format = file_formats[file_format.casefold()]
    if file_format == "JSON":
        data = {
            "n": str(n),
            "e": str(e)
        }
        return json.dumps(data, indent=4).encode("ascii")
    try:
        return RSA.construct((n, e)).exportKey(format=file_format)
    except NotImplementedError as e:
        raise ValueError(f"Cannot create a public key file (key data is incomplete): {(n, e)}") from e


def encode_privkey(n, e, d, p, q, file_format):
    """Encode a public key to file_format

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    d -- RSA private exponent
    p -- RSA first factor
    q -- RSA second factor
    file_format -- file format
    """
    file_format = file_formats[file_format.casefold()]
    if file_format == "JSON":
        data = {
            "n": str(n),
            "e": str(e),
            "d": str(d),
            "p": str(p),
            "q": str(q)
        }
        return json.dumps(data, indent=4).encode("ascii")
    try:
        return RSA.construct((n, e, d, p, q)).exportKey(format=file_format)
    except NotImplementedError as exc:
        raise ValueError(f"Cannot create a private key file (key data is incomplete): {(n, e, d, p, q)}") from exc
