#!/usr/local/bin/sage --python

"""
Sage's primality test
"""

import sys

from sage.all import is_prime, Integer

def factorize_qsieve(n: int) -> None:
    print("[+] Start Primality test")
    if is_prime(n):
        print("[*] The number is prime")
        print()
        sys.exit(1)
    else:
        print("[*] The number is not prime")
        print()
        sys.exit(0)

if __name__ == "__main__":
    factorize_qsieve(Integer(sys.argv[1]))