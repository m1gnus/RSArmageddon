#!/usr/local/bin/sage

##
#   londahl factorization - https://grocid.net/2017/09/16/finding-close-prime-factorizations/  
##

from sage.all import inverse_mod, isqrt, Integer

import os
import sys

"""
londahl custom signal handler
"""

def londahl_handler(sigNum: int, frame: str) -> None:
    print("\n[-] londahl attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, londahl_handler)
signal.signal(signal.SIGINT, londahl_handler)
signal.signal(signal.SIGQUIT, londahl_handler)
signal.signal(signal.SIGILL, londahl_handler)
signal.signal(signal.SIGTRAP, londahl_handler)
signal.signal(signal.SIGABRT, londahl_handler)
signal.signal(signal.SIGBUS, londahl_handler)
signal.signal(signal.SIGFPE, londahl_handler)
signal.signal(signal.SIGUSR1, londahl_handler)
signal.signal(signal.SIGSEGV, londahl_handler)
signal.signal(signal.SIGUSR2, londahl_handler)
signal.signal(signal.SIGPIPE, londahl_handler)
signal.signal(signal.SIGTERM, londahl_handler)
signal.signal(signal.SIGALRM, londahl_handler)

def londahl(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:

    n = Integer(n)

    print("\n[+] Londahl attack started\n")

    # the hypothesis on the private exponent (the theoretical maximum is 0.292)
    b = input("[+] Insert londahl bound (Integer value) (default 10000000): ")
    try: 
        b = int(b) # this means that d < N^delta
        print()
    except ValueError:
        print("[-] Invalid Value, default is setted\n")
        b = 10000000

    phi_approx = n - 2 * isqrt(n) + 1

    look_up = {}
    z = 1

    for i in range(0, b + 1):
        look_up[z] = i
        z = (z * 2) % n

    mu = inverse_mod(Integer(pow(2, phi_approx, n)), n)
    fac = Integer(pow(2, b, n))

    for i in range(0, b + 1):
        if mu in look_up:
            phi = phi_approx + (look_up[mu] - i * b)
            break
        mu = (mu * fac) % n
    else:
        print("[+] Londahl attack failed\n")

    m = n - phi + 1
    roots = ((m - isqrt(m ** 2 - 4 * n)) // 2, (m + isqrt(m ** 2 - 4 * n)) // 2)

    if roots[0] * roots[1] != n:
        print("[+] Londahl attack failed\n")
        sys.exit(1) # exit (failure)
    
    p, q = Integer(roots[0]), Integer(roots[1])

    print(p,q)

    print("[+] Londahl attack complete\n")
    print("[*] p:", p)
    print("[*] q:", q, "\n")

    """
    move PWD in the parent path
    """
    pathname = os.path.dirname(sys.argv[0])
    abspath = os.path.abspath(pathname)
    os.chdir(abspath + "/../")

    """
    create private key file
    """
    if private: # --private
        os.system("sage --python -c 'from misc.software_path import *; import sys; sys.path.append(SOFTWARE_PATH); from pem_utils.certs_manipulation import *; create_privkey(" + str(n) + ", " + str(e) +", None, " + str(p) + ", " + str(q) + ", " + "\"" + str(output_private) + "\"" + ", \"PEM\")'")

    """
    uncipher a specified ciphertext file
    """  
    if ciphertext_file: # --uncipher-file
        os.system("sage --python -c 'from misc.software_path import *; import sys; sys.path.append(SOFTWARE_PATH); from pem_utils.certs_manipulation import *; from parsing.args_filter import *; from cipher_tools.uncipher import *;n, e, d, p, q = fill_privkey_args(" + str(n) + ", " + str(e) + ", None," + str(p) + ", " + str(q) + "); create_privkey(" + str(n) + ", " + str(e) +", None, " + str(p) + ", " + str(q) + ", " + "\"/tmp/tmpprivkey_RSArmageddon.pem\"" + ", \"PEM\"); rsa_uncipher_file(" + "\"" + ciphertext_file + "\"" + ", " + "\"" + output_file + "\"" + ", \"/tmp/tmpprivkey_RSArmageddon.pem\", \"pkcs\"); print(\"[+] Removing temporary private key\")'; rm /tmp/tmpprivkey_RSArmageddon.pem")

    """
    uncipher a specified ciphertext
    """
    if ciphertext: # --uncipher
        os.system("sage --python -c 'from parsing.args_filter import *; from cipher_tools.uncipher import *; n, e, d, p, q = fill_privkey_args(" + str(n) + ", " + str(e) + ", None," + str(p) + ", " + str(q) + "); rsa_uncipher_string(" + "int(\"" + str(ciphertext) + "\")" + ", " + str(n) +", " + "d" + ", None)'")

    sys.exit(0) # exit (success)

if __name__ == "__main__":

    """
    parse the arguments correctly
    """
    n = Integer(sys.argv[1])
    e = Integer(sys.argv[2])
    private = (sys.argv[3] == "True")
    output_private = (None if sys.argv[4] == "None" else sys.argv[4])
    ciphertext_file = (None if sys.argv[5] == "None" else sys.argv[5])
    output_file = sys.argv[6]
    ciphertext = (None if sys.argv[7] == "None" else sys.argv[7])

    londahl(n, e, private, output_private, ciphertext_file, output_file, ciphertext)