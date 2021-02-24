#!/usr/bin/env sage

##
# small factor attack
##

import attack
from attack import positive_int

_, keys = attack.init("Small factor factorization", "small_factor")
n, e, _ = keys[0]

bound = attack.input("Insert upper bound", default=10000000, validator=positive_int)

for i in primes(bound+1):
    if n % i == 0:
        p = i
        q = n // i
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
