#!/usr/local/bin/sage --python

##
#   Fermat_factorizations
#   https://en.wikipedia.org/wiki/Fermat's_factorization_method
##

from sage.all import isqrt, Integer

import sys
import os
import signal

"""
fermat's factorization custom signal handler
"""

seg = 0

def fermat_handler(sigNum: int, frame: str) -> None:
    global seg
    if seg > 0:
        print("[-] Fermat factorization failed\n")
        sys.exit(1) # exit (failure)
    else:
        seg += 1

signal.signal(signal.SIGHUP, fermat_handler)
signal.signal(signal.SIGINT, fermat_handler)
signal.signal(signal.SIGQUIT, fermat_handler)
signal.signal(signal.SIGILL, fermat_handler)
signal.signal(signal.SIGTRAP, fermat_handler)
signal.signal(signal.SIGABRT, fermat_handler)
signal.signal(signal.SIGBUS, fermat_handler)
signal.signal(signal.SIGFPE, fermat_handler)
signal.signal(signal.SIGUSR1, fermat_handler)
signal.signal(signal.SIGSEGV, fermat_handler)
signal.signal(signal.SIGUSR2, fermat_handler)
signal.signal(signal.SIGPIPE, fermat_handler)
signal.signal(signal.SIGTERM, fermat_handler)
signal.signal(signal.SIGALRM, fermat_handler)

def fermat_factorization(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:
    
    print("[+] Fermat factorization started")

    a = isqrt(n)
    b2 = a*a - n
    b = a

    while b*b != b2:
        a = a + 1
        b2 = a*a - n
        b = isqrt(b2)

    p = a+b
    q = a-b

    if n != (p*q):
        print("[-] Fermat factorization failed: n != p * q\n")
        sys.exit(1) # exit (failure)

    print("[+] Fermat factorization complete\n")
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

    fermat_factorization(n, e, private, output_private, ciphertext_file, output_file, ciphertext)

