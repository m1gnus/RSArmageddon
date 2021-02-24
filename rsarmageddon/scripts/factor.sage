#!/usr/bin/env sage

import sys
import output

n = Integer(sys.argv[1])
output.init(sys.argv[2])

output.success("Start Factorization")
results = factor(n)
output.success("Factorization complete")
for fact, exp in results:
    output.primary("{}^{}".format(fact, exp))
