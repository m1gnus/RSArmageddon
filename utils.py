import sys
import json
import hashlib

from functools import partial
from contextlib import redirect_stdout
from gmpy2 import invert, isqrt


DEFAULT_E = 65537


def byte_length(n: int) -> int:
    """Return byte length of the given integer

    Arguments:
    n -- int
    """
    return -(n.bit_length() // -8)


def to_bytes_auto(n: int) -> bytes:
    """Convert int to shortest possible bytes object, big endian

    Arguments:
    n -- int
    """
    return n.to_bytes(byte_length(n), "big")


def compute_extra_key_elements(d: int, p: int, q: int) -> tuple:
    """Compute extra key elements

    Arguments:
    d -- RSA private exponent
    p -- RSA first factor
    q -- RSA second factor
    """
    if d is not None:
        dp = d%(p-1)
        dq = d%(q-1)
    else:
        dp, dq = None, None
    if p is not None and q is not None:
        pinv = int(invert(p, q))
        qinv = int(invert(q, p))
    else:
        pinv, qinv = None, None

    return dp, dq, pinv, qinv


def compute_pubkey(n: int, e: int, d: int, p: int, q: int, phi=None) -> tuple:
    """Compute public key elements

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    d -- RSA private exponent
    p -- RSA first factor
    q -- RSA second factor
    """

    tup = (n, e, d, p, q)

    pks = set()

    if n is not None and e is not None:
        set.add((n, e))

    if n is not None and d is not None:
        if phi is not None:
            set.add((n, invert(d, phi)))
        else:
            if p is None:
                p = q
            if p is not None:
                q = n//p
                set.add((n, invert(d, (p-1) * (q-1))))

    if p is not None and q is not None:
        if d is not None:
            set.add((p*q, invert(d, (p-1) * (q-1))))
        if e is not None:
            set.add((p*q, e))

    if len(pks) != 1:
        raise ValueError(f"Inconsistent parameters {tup}")

    return pks.pop()


def complete_privkey(n: int, e: int, d: int, p: int, q: int, phi=None) -> tuple:
    """Compute missing private key elements

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    d -- RSA private exponent
    p -- RSA first factor
    q -- RSA second factor
    """

    tup = (n, e, d, p, q, phi)

    if n is None and (p is None or q is None):
        raise ValueError(f"You have to provide n or both p and q in tuple '{tup}'")
    elif n is not None and (p is None and q is None and phi is None):
        raise ValueError(f"If you provide n, you must provide also p, q or phi in tuple '{tup}'")
    elif e is None and d is None:
        raise ValueError(f"You have to provide e or d in tuple '{tup}'")

    if n is not None and p is None and q is None and phi is not None:
        p = ((n + 1 - phi) - isqrt((n + 1 - phi)**2 - 4*n)) // 2

    if n is None:
        n = p*q
    elif p is None:
        p = n//q
    elif q is None:
        q = n//p

    if n != p * q:
        raise ValueError(f"n is not equal to p * q in tuple '{tup}'")

    phi = (p-1) * (q-1)

    if e is None:
        e = int(invert(d, phi))
    elif d is None:
        d = int(invert(e, phi))

    return n, e, d, p, q

def compute_d(n: int, e: int, d: int, p: int, q: int, phi=None) -> int:
    """Compute d from available parameters

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    d -- RSA private exponent
    p -- RSA first factor
    q -- RSA second factor
    """

    tup = (n, e, d, p, q, phi)

    ds = set()

    if d is not None:
        ds.add(d)

    if e is None:
        raise ValueError(f"Missing public exponent")

    if phi is not None:
        ds.add(invert(e, phi))

    if p is None:
        p = q

    if p is not None:
        if q is not None:
            ds.add(invert(e, (p-1) * (q-1)))
        if n is not None:
            q = n//p
            ds.add(invert(e, (p-1) * (q-1)))

    if len(ds) != 1:
        raise ValueError(f"Inconsistent parameters {tup}")

    return ds.pop()


def compute_n(n: int, e: int, d: int, p: int, q: int, phi=None) -> int:
    """Compute d from available parameters

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    d -- RSA private exponent
    p -- RSA first factor
    q -- RSA second factor
    """

    tup = (n, e, d, p, q, phi)

    ns = set()

    if n is not None:
        ns.add(n)

    if p is not None and q is not None:
        ns.add(p*q)

    if p is None:
        p = q

    if phi is not None and p is not None:
        ns.add((pow(p, 2) - p + p*phi) // (p-1))

    if len(ns) != 1:
        raise ValueError(f"Inconsistent parameters {tup}")

    return ns.pop()


def output_cleartext(text, filename, json_output=False):
    text_raw = to_bytes_auto(text)
    if filename is True:
        text_hex = f"0x{text_raw.hex()}"
        if json_output:
            json.dump({
                "output": str(output),
                "dec": str(output),
                "hex": text_hex,
                "raw": str(text_raw)
            }, sys.stdout, indent=4)
        else:
            with redirect_stdout(sys.stderr):
                print(f"[+] ciphertext (dec): {text}")
                print(f"[+] ciphertext (hex): {text_hex}")
                print(f"[+] ciphertext (raw): {text_raw}")
                print()
    else:
        with open(filename, "wb") as file:
            file.write(text_raw)


# From a tip I saw here: https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def file_checksum(path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(partial(f.read, 4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
