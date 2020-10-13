#!/usr/bin/env sage

##
#   Wiener_Factorization_attack
#   https://en.wikipedia.org/wiki/Wiener%27s_attack
##

import attack

attack.init("Wiener factorization")

_, keys = attack.get_args()
n, e, _ = keys[0]

n = Integer(n)
e = Integer(e)

cf_convergents = continued_fraction(e/n).convergents()

for el in cf_convergents:
    k = Integer(el.numerator())
    d = Integer(el.denominator())

    if k == 0 or (e*d - 1) % k != 0:
        continue

    phi = (e*d - 1)//k
    s = n - phi + 1
    delta = s*s - 4*n

    # If delta >= 0 then we have 2 real solutions
    if (delta < 0
            or not delta.is_integer()
            or not delta.is_square()
            or is_odd(s + isqrt(delta))):
        continue

    x = var('x')
    roots = solve(x**2 - s*x + n, x)
    p = roots[0].rhs()
    q = roots[1].rhs()

    if p < 0 or q < 0:
        continue

    if p * q == n:
        attack.info(f"p:", p)
        attack.info(f"q:", q)
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
