#!/usr/local/bin/sage --python

"""
general purpose factorization with ecm
"""

from sys import argv

from sage.all import euler_phi, Integer

def euler_phi_calc(n: int) -> None:
    print("[+] Start calculating euler's phi of", n, "\n")
    res = euler_phi(n)
    print("[*]", res, "\n")
    print("[+] Success!")

if __name__ == "__main__":
    euler_phi_calc(Integer(argv[1]))
