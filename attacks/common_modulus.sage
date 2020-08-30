#!/usr/local/bin/sage

##
#   Common Modulus
##

from sage.all import xgcd, Integer

import os
import sys
import signal
import binascii

"""
common modulus custom signal handler
"""

def cm_handler(sigNum: int, frame: str) -> None:
    print("\n[-] common factor attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, cm_handler)
signal.signal(signal.SIGINT, cm_handler)
signal.signal(signal.SIGQUIT, cm_handler)
signal.signal(signal.SIGILL, cm_handler)
signal.signal(signal.SIGTRAP, cm_handler)
signal.signal(signal.SIGABRT, cm_handler)
signal.signal(signal.SIGBUS, cm_handler)
signal.signal(signal.SIGFPE, cm_handler)
signal.signal(signal.SIGUSR1, cm_handler)
signal.signal(signal.SIGSEGV, cm_handler)
signal.signal(signal.SIGUSR2, cm_handler)
signal.signal(signal.SIGPIPE, cm_handler)
signal.signal(signal.SIGTERM, cm_handler)
signal.signal(signal.SIGALRM, cm_handler)

def common_modulus(n: int, e1: int, e2: int, c1: int, c2: int) -> None:
    print("\n[+] Common modulus attack started")

    if (e1 == e2):
        print("[-] e1 and e2 has to be different, common modulus attack failed\n")
        sys.exit(1)
    
    _, u, v = xgcd(e1, e2)

    m = pow(c1, u, n) * pow(c2, v, n)
    hexm = hex(m)

    print("[+] m (dec):", m)
    print("[+] m (hex):", hexm)
    print("[+] m (raw):", binascii.unhexlify(hexm), "\n")

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
