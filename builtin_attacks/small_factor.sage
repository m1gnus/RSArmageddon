#!/usr/bin/env sage

##
# small factor attack
##

import attack

attack.init("Small factor factorization")

_, keys = attack.get_args()
n, e, _ = keys[0]

def positive_int(s):
    i = int(s)
    if i <= 0:
        raise ValueError("Must be a positive number")
    return i

bound = attack.input("Insert upper bound", default=10000000, validator=positive_int)

for i in primes(bound+1):
    if n % i == 0:
        p = i
        q = n // i
        attack.info("p:", p)
        attack.info("q:", q)
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
