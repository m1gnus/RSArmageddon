#!/usr/bin/env sage

##
#   Common factor attack
#   https://www.slideshare.net/VineetKumar130/common-factor-attack-on-rsa
##

from multiprocessing import Pool
from itertools import combinations

import attack


def common_factor(indices):
    i, j = indices
    n1, e1, name1 = keys[i]
    n2, e2, name2 = keys[j]
    p = gcd(n1, n2)
    if p != 1:
        q1 = n1//p
        q2 = n2//p
        return n1, e1, n2, e2, p, q1, q2, name1, name2


attack.init("Common factor")

_, keys = attack.get_args(min_keys=2)

found = False

with Pool() as pool:
    indices = combinations(range(len(keys)), 2)
    for ret in pool.imap_unordered(common_factor, indices, chunksize=10000):
        if ret is not None:
            found = True
            n1, e1, n2, e2, p, q1, q2, name1, name2 = ret
            attack.info("p:", p)
            attack.info("q:", q1)
            attack.info("p:", p)
            attack.info("q:", q2)
            attack.keys(
                    (n1, e1, None, p, q1, name1),
                    (n2, e2, None, p, q2, name2))

if found:
    attack.success()
else:
    attack.fail()
