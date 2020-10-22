#!/usr/bin/env sage

##
#   Fermat_factorizations
#   https://en.wikipedia.org/wiki/Fermat's_factorization_method
##


import attack

attack.init("Fermat factorization", "fermat")

_, keys = attack.get_args()
n, e, _ = keys[0]

a = isqrt(n)
b2 = a*a - n
b = a

while b*b != b2:
    a = a + 1
    b2 = a*a - n
    b = isqrt(b2)

p = a+b
q = a-b

if n != (p*q):
    attack.fail("n != p * q")

attack.keys((n, e, None, p, q))
attack.success()
