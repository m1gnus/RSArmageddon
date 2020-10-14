#!/usr/bin/env sage

##
# Novelty Primes - Most numbers in the form 31(3*)7 are prime numbers
##

import attack

attack.init("Novelty primes factorization")

_, keys = attack.get_args()
n, e, _ = keys[0]

def positive_int(s):
    i = int(s)
    if i <= 0:
        raise ValueError("Must be a positive number")
    return i

bound = attack.input("Insert upper bound: max number of digits", default=1000000, validator=positive_int)
bound = min(bound, int(log(n, 10)+1))

for i in range(bound-4):
    p = int("313{}7".format("3"*i))
    q, r = divmod(n, p)
    if not r:
        attack.info("p:", p)
        attack.info("q:", q)
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
