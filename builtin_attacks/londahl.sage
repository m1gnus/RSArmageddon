#!/usr/bin/env sage

##
#   londahl factorization - https://grocid.net/2017/09/16/finding-close-prime-factorizations/
##

import attack
from attack import positive_int

attack.init("Londahl factorization")

_, keys = attack.get_args()
n, e, _ = keys[0]

n = Integer(n)
e = Integer(e)

R = Integers(n)

b = attack.input("Insert londahl bound", default=20000000, validator=positive_int)

phi_approx = n - 2 * isqrt(n) + 1

discrete_logs = {}
z = 1
for i in range(0, b + 1):
   discrete_logs[z] = i
   z = (z * 2) % n

mu = R(inverse_mod(power_mod(2, phi_approx, n), n))
fac = power_mod(2, b, n)

for i in range(0, b^2 + 1, b):
    log = discrete_logs.get(mu)
    if log is not None:
        phi = phi_approx + (log - i)
        break
    mu *= fac
else:
    attack.fail()

m = n - phi + 1
p = Integer((m - isqrt(m^2 - 4*n)) // 2)
q = Integer((m + isqrt(m^2 - 4*n)) // 2)

if p * q != n:
    attack.fail()

attack.keys((n, e, None, p, q))
attack.success()
