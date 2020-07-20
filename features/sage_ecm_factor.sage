#!/usr/local/bin/sage --python

"""
general purpose factorization with ecm
"""

from sys import argv
from subprocess import check_output

from sage.all import ecm, Integer

def factorize_ecm(n: int) -> None:
    print("[+] Start Factorization with ECM method")
    results = list(ecm.factor(n))
    results_set = set(results)
    print("[+] Factorization complete\n")
    for fact in results_set:
        print("[*] " + str(fact) + "^" + str(results.count(fact)))
    print()

if __name__ == "__main__":
    factorize_ecm(Integer(argv[1]))