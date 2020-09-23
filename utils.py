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
