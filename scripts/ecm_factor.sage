#!/usr/bin/env sage

import sys
from itertools import groupby

import output


n = Integer(sys.argv[1])
output.success("Start Factorization with ECM method")
results = groupby(ecm.factor(n))
output.success("Factorization complete")
for fact, exp in results:
    output.primary("{}^{}".format(fact, len(tuple(exp))))
