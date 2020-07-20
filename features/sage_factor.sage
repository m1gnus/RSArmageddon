#!/usr/local/bin/sage --python

"""
general purpose factorization
"""

from sys import argv

from sage.all import factor, Integer

def factorize(n: int) -> None:
    print("[+] Start Factorization")
    results = str(factor(n)).split(" * ")
    print("[+] Factorization complete\n")
    for fact in results:
        print("[*] " + fact)
    print()

if __name__ == "__main__":
    factorize(Integer(argv[1]))