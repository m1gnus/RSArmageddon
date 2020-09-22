#!/usr/bin/env sage

##
# Qicheng general purpose factorization algorithm - https://www.cs.ou.edu/~qcheng/paper/speint.pdf
# script taken from https://github.com/Ganapati/RsaCtfTool/blob/master/sage/qicheng.sage
##

import sys

# dangerous: may crash the interpreter
# no big deal since we are running in a subinterpreter
sys.setrecursionlimit(100000)

import attack

attack.init("Qi Cheng factorization")

ciphertext, nes = attack.get_args()
n, e = nes[0]

ATTEMPTS = 20

R = Integers(n)
js = (0, (-2^5)^3, (-2^5*3)^3, (-2^5*3*5*11)^3, (-2^6*3*5*23*29)^3)
p, q = None, None

for j in js * ATTEMPTS:
    if not j:
        a = R.random_element()
        E = EllipticCurve([0, a])
    else:
        a = R(j)/(R(1728)-R(j))
        c = R.random_element()
        E = EllipticCurve([3*a*c^2, 2*a*c^3])

    x = R.random_element()
    z = E.division_polynomial(n, x)
    g = gcd(z, n)

    if g > 1:
        p = Integer(g)
        q = Integer(n)//p
        attack.info(f"p: {p}")
        attack.info(f"q: {q}")
        attack.success((n, e, None, p, q))

attack.fail()
