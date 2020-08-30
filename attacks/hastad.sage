#!/usr/local/bin/sage

##
# hastad broadcast attack - https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-Hastad-Broadcast
##

import sys
import os
import binascii
import signal

"""
hastad custom signal handler
"""

def hastad_handler(sigNum: int, frame: str) -> None:
    print("\n[-] hastad attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, hastad_handler)
signal.signal(signal.SIGINT, hastad_handler)
signal.signal(signal.SIGQUIT, hastad_handler)
signal.signal(signal.SIGILL, hastad_handler)
signal.signal(signal.SIGTRAP, hastad_handler)
signal.signal(signal.SIGABRT, hastad_handler)
signal.signal(signal.SIGBUS, hastad_handler)
signal.signal(signal.SIGFPE, hastad_handler)
signal.signal(signal.SIGUSR1, hastad_handler)
signal.signal(signal.SIGSEGV, hastad_handler)
signal.signal(signal.SIGUSR2, hastad_handler)
signal.signal(signal.SIGPIPE, hastad_handler)
signal.signal(signal.SIGTERM, hastad_handler)
signal.signal(signal.SIGALRM, hastad_handler)

def hastad(n1: int, n2: int, n3: int, e: int, c1: int, c2: int, c3: int) -> None:

    c4 = crt([c1, c2, c3], [n1, n2, n3])

    m = c4.nth_root(e)
    hexm = hex(m)

    print("[+] m (dec):", m)
    print("[+] m (hex):", hexm)
    print("[+] m (raw):", binascii.unhexlify(hexm[2:]), "\n")


"""
Given a list of numbers, check if at least one number in the list is repeated
"""
def same_number_check(n: list) -> bool:
    for i in n:
        if n.count(i) != 1:
            return True
        else:
            return False

if __name__ == "__main__":

    """
    parse the arguments correctly
    """
    n = [Integer(x) for x in sys.argv[1].split(":") if x]
    e = [Integer(x) for x in sys.argv[2].split(":") if x]

    if len(n) < 3 or same_number_check(n):
        print("[-] Hastad's broadcast attack requires 3 different RSA modulus")
        sys.exit(1) # exit (failure)

    n = n[:3]
    e = e[0]
    
    c1 = Integer(input("Insert c1 (decimal): "))
    c2 = Integer(input("Insert c2 (decimal): "))
    c3 = Integer(input("Insert c3 (decimal): "))
    print()

    hastad(*n, e, c1, c2, c3)