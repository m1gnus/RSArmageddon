from gmpy2 import invert

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


def complete_privkey(n: int, e: int, d: int, p: int, q: int) -> tuple:
    """Compute missing private key elements

    Arguments:
    n -- RSA modulus
    e -- RSA public exponent
    d -- RSA private exponent
    p -- RSA first factor
    q -- RSA second factor
    """

    """
    check that the required arguments is setted
    """

    tup = (n, e, d, p, q)

    if n is None and (p is None or q is None):
        raise ValueError(f"You have to provide n or both p and q in tuple '{tup}'")
    elif n is not None and (p is None and q is None):
        raise ValueError(f"If you provide n, you must provide also p or q in tuple '{tup}'")
    elif e is None and d is None:
        raise ValueError(f"You have to provide e or d in tuple '{tup}'")

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
