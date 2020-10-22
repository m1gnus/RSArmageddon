import sys
import json

from contextlib import redirect_stdout
from pathlib import Path

from gmpy2 import invert
from Crypto.PublicKey import RSA

from utils import DEFAULT_E


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


def print_key(n=None, e=None, d=None, p=None, q=None, dp=None, dq=None, pinv=None, qinv=None, file=None):
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

    if file is None:
        file = sys.stdout

    with redirect_stdout(file):
        print(f"[*] n: {n}")
        print(f"[*] e: {e}")
        print(f"[*] d: {d}")
        print(f"[*] p: {p}")
        print(f"[*] q: {q}")
        print()
        print(f"[#] dp: {dp}")
        print(f"[#] dq: {dq}")
        print(f"[#] pinv: {pinv}")
        print(f"[#] qinv: {qinv}")
        print()


def print_key_json(n=None, e=None, d=None, p=None, q=None, dp=None, dq=None, pinv=None, qinv=None, file=None):
    d = {k: str(v) for k, v in locals().items()}
    del d["file"]
    json.dump(d, file, indent=4)
    print(file=file)


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


def load_keys(path, exts):
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

        for key_file in path.glob(f"*{ext}"):
            n, e, _, _, _ = load_key(key_file)
            keys.append(((n, e), key_file.stem))

    return keys


file_formats = {
    "pem": "PEM",
    "der": "DER",
    "openssh": "OpenSSH"
}


def encode_pubkey(n, e, file_format):
    """Encode a public key to file_format

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    file_format -- file format
    """
    file_format = file_formats[file_format.casefold()]
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
    try:
        return RSA.construct((n, e, d, p, q)).exportKey(format=file_format)
    except NotImplementedError as e:
        raise ValueError(f"Cannot create a private key file (key data is incomplete): {(n, e, d, p, q)}") from e
