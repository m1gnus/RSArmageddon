#!/usr/bin/env sage

import sys

n = Integer(sys.argv[1])
print("[+] Start Factorization", file=sys.stderr)
results = factor(n)
print("[+] Factorization complete", file=sys.stderr)
for fact, exp in results:
    print("[*] {}^{}".format(fact, exp), file=sys.stderr)