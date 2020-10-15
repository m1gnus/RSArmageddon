#!/usr/bin/env sage

##
# small fraction attack (p/q cloe to a small fraction) - from https://github.com/Ganapati/RsaCtfTool/blob/master/sage/smallfraction.sage
##

import attack

attack.init("Small fraction factorization")

_, keys = attack.get_args()
n, e, _ = keys[0]

def positive_int(s):
    i = int(s)
    if i <= 0:
        raise ValueError("Must be a positive number")
    return i

depth = attack.input("Insert depth", default=50, validator=positive_int)

x = PolynomialRing(Zmod(n), "x").gen()

p, q = None, None

for den in IntegerRange(2, depth+1):
    for num in IntegerRange(1, den):
        if gcd(num, den) != 1:
            continue

        r = den / num
        phint = isqrt(n * r)
        f = x - phint
        sr = f.small_roots(beta=0.5)

        if len(sr) <= 0:
            continue

        p = (phint - sr[0]).lift()
        if n % p == 0:
            q = n // p
            attack.info("p:", p)
            attack.info("q:", q)
            attack.keys((n, e, None, p, q))
            attack.success()

attack.fail()