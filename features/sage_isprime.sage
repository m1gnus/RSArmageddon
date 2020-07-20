#!/usr/local/bin/sage --python

"""
Sage's primality test
"""

from sys import argv

from sage.all import is_prime, Integer

def factorize_qsieve(n: int) -> None:
    print("[+] Start Primality test")
    if is_prime(n):
        print("[*] The number is prime")
    else:
        print("[*] The number is not prime")
    print()

if __name__ == "__main__":
    factorize_qsieve(Integer(argv[1]))