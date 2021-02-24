#!/usr/bin/env sage

##
#   FactorDB factorization
#   http://factordb.com/
##

import attack

import json
from urllib import request


URL = "http://factordb.com/api"

_, keys = attack.init("FactorDB factorization", "factordb")
n, e, _ = keys[0]

with request.urlopen(f"{URL}?query={n}") as response:
    response = json.load(response)

factors = [(int(f), n) for f, n in response["factors"]]
status = response["status"]
n_factors = sum(n for _, n in factors)

if status == "FF":
    if len(factors) == 2 and n_factors == 2:
        p, _ = factors[0]
        q, _ = factors[1]
        attack.keys((n, e, None, p, q))
        attack.success()
    else:
        attack.fail("Invalid factors:", factors, bad_key=True)
elif status == "P":
    attack.fail("Number is prime:", n, bad_key=True)
elif status == "CF":
    if n_factors > 2:
        attack.fail("Partially factorized, but too many factors found:", factors, bad_key=True)
    else:
        attack.fail("Partially factorized, only one factor found:", factors)
else:
    attack.fail()
