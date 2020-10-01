#!/usr/bin/env sage

import sys


n = Integer(sys.argv[1])
print("[+] Start Primality test", file=sys.stderr)
if is_prime(n):
    print("[*] The number is prime", file=sys.stderr)
else:
    print("[*] The number is not prime", file=sys.stderr)
