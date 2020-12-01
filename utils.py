import sys
import json
import random
import hashlib

from functools import partial
from contextlib import redirect_stdout
from base64 import b64encode, urlsafe_b64encode
from gmpy2 import invert, isqrt, gcd


DEFAULT_E = 65537


def carmichael_lcm(p, q):
    phi = (p-1)*(q-1)
    return phi // gcd(p-1, q-1)


def byte_length(n):
    """Return byte length of the given integer

    Arguments:
    n -- int
    """
    return -(n.bit_length() // -8)


def to_bytes_auto(n):
    """Convert int to shortest possible bytes object, big endian

    Arguments:
    n -- int
    """
    return n.to_bytes(byte_length(n), "big")


def int_from_path(path):
    with open(path, "rb") as f:
        return int.from_bytes(f.read(), "big")


def compute_extra_key_elements(d, p, q):
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


def compute_pubkey(n, e, d, p, q, phi=None):
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
        pks.add((n, e))

    if n is not None and d is not None:
        if phi is not None:
            tmp_e = int(invert(d, phi))
            pks.add((n, tmp_e))
        else:
            if p is None:
                p = q
            if p is not None:
                q = n//p
                phi =  (p-1) * (q-1)
                tmp_e = int(invert(d, phi))
                if e is not None and tmp_e != e:
                    tmp_e = int(invert(d, phi//gcd(p-1,q-1)))
                pks.add((n, tmp_e))

    if p is not None and q is not None:
        if d is not None:
            phi =  (p-1) * (q-1)
            tmp_e = int(invert(d, phi))
            if e is not None and tmp_e != e:
                tmp_e = int(invert(d, phi//gcd(p-1,q-1)))
            pks.add((p*q, tmp_e))

    if len(pks) != 1:
        raise ValueError(f"Inconsistent parameters {tup}")

    return pks.pop()


def recover_pq(n, e, d):
    k = d*e - 1

    if k % 2 != 0:
        raise ValueError(f"p and q cannot be recovered from these parameters {(n, e, d)}")

    factor = 1
    while k % 2 == 0:
        factor *= 2
        k //= 2

    for i in range(100):
        b = 0
        g = random.randint(0, n)
        y = pow(g, k, n)
        if y == 1 or y == (n - 1):
            continue
        for j in range(1, factor):
            x = pow(y, 2, n)
            if x in (1, n-1):
                break
            y = x
        else:
            x = pow(y, 2, n)
        if x == 1:
            break
    else:
        raise ValueError(f"p and q cannot be recovered (not enough iterations?)")

    p = int(gcd(y-1, n))
    q = n // p
    return p, q


def complete_privkey(n, e, d, p, q, phi=None, use_lcm=True):
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
    if n is not None and (p is None and q is None and phi is None) and (d is None or e is None):
        raise ValueError(f"If you provide n, you must provide also either one of p, q or phi, or d and e, in tuple '{tup}'")
    if e is None and d is None:
        raise ValueError(f"You have to provide e or d in tuple '{tup}'")

    if n is not None and p is None and q is None and phi is not None:
        p = ((n + 1 - phi) - isqrt((n + 1 - phi)**2 - 4*n)) // 2

    if n is None:
        n = p*q
    elif p is None:
        p = n//q
    elif q is None:
        q = n//p

    if p is None:
        p, q = recover_pq(n, e, d)

    if n != p * q:
        raise ValueError(f"n is not equal to p * q in tuple '{tup}'")

    if use_lcm:
        phi = carmichael_lcm(p, q)
    else:
        phi = (p-1) * (q-1)

    if e is None:
        e = int(invert(d, phi))
    elif d is None:
        d = int(invert(e, phi))

    return n, e, d, p, q

def compute_d(n, e, d, p, q, phi=None):
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

    if e is None and len(ds) == 0:
        raise ValueError("Missing public exponent")

    if phi is not None:
        ds.add(int(invert(e, phi)))

    if p is None:
        p = q

    if p is not None:
        if q is not None:
            tmp_d = int(invert(e, (p-1) * (q-1)))
            if d is not None and tmp_d != d:
                tmp_d = int(invert(e, carmichael_lcm(p, q)))
            ds.add(tmp_d)
        if n is not None:
            q = n//p
            tmp_d = int(invert(e, (p-1) * (q-1)))
            if d is not None and tmp_d != d:
                tmp_d = int(invert(e, carmichael_lcm(p, q)))
            ds.add(tmp_d)

    if len(ds) != 1:
        raise ValueError(f"Inconsistent parameters {tup}")

    return ds.pop()


def compute_n(n, e, d, p, q, phi=None):
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


def output_text(label, text, filename, encoding=None, json_output=False):
    text_raw = to_bytes_auto(text)
    text_b64 = b64encode(text_raw).decode("ascii")
    text_b64_url = urlsafe_b64encode(text_raw).decode("ascii")
    if encoding is not None:
        try:
            text_str = text_raw.decode(encoding)
        except ValueError:
            text_str = f"Cannot decode ({encoding})"
    else:
        text_str = None
    if filename is True:
        text_hex = f"0x{text_raw.hex()}"
        if json_output:
            output = {
                "dec": str(text),
                "hex": text_hex,
                "raw": str(text_raw),
                "b64": str(text_b64),
                "url": str(text_b64_url)
            }
            if text_str is not None:
                output["str"] = text_str
            json.dump(output, sys.stdout, indent=4)
        else:
            with redirect_stdout(sys.stderr):
                print(f"[+] {label} (dec): {text}")
                print(f"[+] {label} (hex): {text_hex}")
                print(f"[+] {label} (raw): {text_raw}")
                print(f"[+] {label} (b64): {text_b64}")
                print(f"[+] {label} (url): {text_b64_url}")
                if text_str is not None:
                    print(f"[+] {label} (str): {text_str}")
    else:
        with open(filename, "wb") as file:
            file.write(text_raw)


# From a tip I saw here: https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def file_checksum(filename):
    hash_sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(partial(f.read, 4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
