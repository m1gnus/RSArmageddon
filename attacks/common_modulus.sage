#!/usr/local/bin/sage

##
#   Common Modulus
##

from sage.all import xgcd, Integer
import os, sys

def common_modulus(n: int, e1: int, e2: int, c1: int, c2: int) -> None:
    print("\n[+] Common modulus attack started")

    if (e1 == e2):
        print("[-] e1 and e2 has to be different, common modulus attack failed\n")
        sys.exit(1)
    
    _, u, v = xgcd(e1, e2)

    m = pow(c1, u, n) * pow(c2, v, n)

    print("[+] m:", m, "\n")

    sys.exit(1)


if __name__ == "__main__":

    """
    parse the arguments correctly
    """
    n = [Integer(x) for x in sys.argv[1].split(":") if x][0]
    e = [Integer(x) for x in sys.argv[2].split(":") if x]

    if len(e) != 2:
        print("\n[-] For common modulus attack exactly 2 values of e is required\n")
        sys.exit(1) # exit (failure)
    
    c1 = Integer(input("Insert c1 (decimal): "))
    c2 = Integer(input("Insert c2 (decimal): "))

    common_modulus(n, e[0], e[1], c1, c2)
