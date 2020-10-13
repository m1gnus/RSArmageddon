#!/usr/bin/env sage

##
# hastad broadcast attack - https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-Hastad-Broadcast
##

from itertools import combinations

import attack

attack.init("Hastad broadcast")

ciphertexts, keys = attack.get_args(min_keys=3, min_ciphertexts=3, deduplicate=True)
ns, es, _ = tuple(zip(*keys))
cs, _ = tuple(zip(*ciphertexts))
_, name = ciphertexts[0]

if len(ns) != len(cs):
    attack.fail("Number of ciphertexts and public keys differ")

if not len(set(es)) == 1:
    attack.fail("RSA exponents differ")

e = Integer(es[0])

if len(ns) > 20:
    attack.info("Too many messages, skipping safety pairwise GCD check, results may be inconsistent")
elif any(gcd(a, b) != 1 for a, b in combinations(ns, 2)):
    attack.fail("Public key moduli are not coprime")

c4 = crt([Integer(c) for c in cs], [Integer(n) for n in ns])

m = c4.nth_root(e)

attack.cleartexts((m, name))
attack.success()
