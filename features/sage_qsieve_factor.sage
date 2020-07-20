#!/usr/local/bin/sage --python

"""
general purpose factorization with qsieve factorization method
"""

from sys import argv

from sage.all import qsieve, Integer

def factorize_qsieve(n: int) -> None:
    print("[+] Start Factorization with qsieve method")
    try:
        if len(str(n)) < 40:
            raise ValueError("In order to perform qsieve factorization the integer must have at least 40 digits")
    except ValueError as e:
        print("sage_qsieve_factor.sage:factorize_qsieve ->",e)
        exit(1)
        
    results = list(qsieve(n)[0])
    results_set = set(results)
    print("[+] Factorization complete\n")
    for fact in results_set:
        print("[*] " + str(fact) + "^" + str(results.count(fact)))
    print()

if __name__ == "__main__":
    factorize_qsieve(Integer(argv[1]))