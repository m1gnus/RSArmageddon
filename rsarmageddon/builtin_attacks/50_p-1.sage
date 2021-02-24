#!/usr/bin/env sage

##
#   p-1 pollard
#   https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm
##

import attack

_, keys = attack.init("Pollard's p-1 factorization", "pollard_p_1")
n, e, _ = keys[0]

B = isqrt(n)

x = 1

for k in primes(100000):
    for _ in range(integer_floor(log(B, k))):
        x *= k
        p = gcd(power_mod(2, x, n)-1, n)
        if p in range(2, n):
            q = n//p
            attack.keys((n, e, None, p, q))
            attack.success()

attack.fail()
