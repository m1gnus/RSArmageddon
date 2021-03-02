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
import random
import hashlib
import importlib
import importlib.machinery

from pathlib import Path
from shutil import copyfileobj
from functools import partial
from contextlib import redirect_stdout
from importlib import resources, import_module
from base64 import b64encode, urlsafe_b64encode
from gmpy2 import invert, isqrt, gcd

from . import output


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
        if e is not None:
            pks.add((p*q, e))

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
            output_obj = {
                "dec": str(text),
                "hex": text_hex,
                "raw": str(text_raw),
                "b64": str(text_b64),
                "url": str(text_b64_url)
            }
            if text_str is not None:
                output_obj["str"] = text_str
            json.dump(output_obj, sys.stdout, indent=4)
        else:
            with redirect_stdout(sys.stderr):
                output.primary(f"{label} (dec): {text}")
                output.primary(f"{label} (hex): {text_hex}")
                output.primary(f"{label} (raw): {text_raw}")
                output.primary(f"{label} (b64): {text_b64}")
                output.primary(f"{label} (url): {text_b64_url}")
                if text_str is not None:
                    output.primary(f"{label} (str): {text_str}")
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


def module_root(m):
    mpath = Path(m.__file__)
    if mpath.stem == "__init__":
        mpath = mpath.parent
    return mpath


def copy_resource(package, res, dest):
    with resources.open_binary(package, res) as src, \
            open(Path(dest)/res, "wb") as dst:
        copyfileobj(src, dst)


def copy_resource_module(package, module, dest):
    suffs = importlib.machinery.all_suffixes()
    for res in resources.contents(package):
        if not resources.is_resource(package, res):
            continue
        try:
            name, ext = res.rsplit(".", maxsplit=1)
        except ValueError:
            continue
        if name == module and f".{ext}" in suffs:
            copy_resource(package, res, dest)
            return
    else:
        raise ValueError(f"No such module {module!r} in package {package}")


def copy_resource_tree(package, dest):
    package_name = package.__name__.split(".")[-1]
    dest_subdir = Path(dest)/package_name
    dest_subdir.mkdir(mode=0o755, exist_ok=True)
    for x in resources.contents(package):
        if resources.is_resource(package, x):
            copy_resource(package, x, dest_subdir)
        elif x != "__pycache__":
            subpackage = import_module(f".{x}", package.__name__)
            copy_resource_tree(subpackage, dest_subdir)
