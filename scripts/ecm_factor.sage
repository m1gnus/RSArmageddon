#!/usr/bin/env sage

import sys
from itertools import groupby


n = Integer(sys.argv[1])
print("[+] Start Factorization with ECM method", file=sys.stderr)
results = groupby(ecm.factor(n))
print("[+] Factorization complete", file=sys.stderr)
for fact, exp in results:
    print("[*] {}^{}".format(fact,len(tuple(exp))), file=sys.stderr)