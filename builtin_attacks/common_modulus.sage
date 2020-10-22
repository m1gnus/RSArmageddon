#!/usr/bin/env sage

##
#   Common Modulus
##

import attack

attack.init("Common modulus", "common_modulus")

ciphertexts, keys = attack.get_args(min_keys=2, min_ciphertexts=2)
n1, e1, _ = keys[0]
n2, e2, _ = keys[1]
c1, name = ciphertexts[0]
c2, _ = ciphertexts[1]

if n1 != n2:
    attack.fail("n1 and n2 have to be the same")

n = n1

if gcd(e1, e2) != 1:
    attack.fail("e1 and e2 are not coprime")

_, u, v = xgcd(e1, e2)

m = pow(c1, u, n) * pow(c2, v, n)

attack.cleartexts((m, name))
attack.success()
