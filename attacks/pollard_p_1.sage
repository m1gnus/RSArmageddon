#!/usr/local/bin/sage --python

##
#   p-1 pollard
#   https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm
##

from sage.all import gcd, factorial, isqrt, is_prime, log, floor, Integer

import sys
import os
import signal
import time

"""
p_1 factorization's custom signal handler
"""

seg = 0

def p_1_handler(sigNum: int, frame: str) -> None:
    global seg
    if seg > 0:
        print("[-] pollard p-1 factorization failed\n")
        sys.exit(1) # exit (failure)
    else:
        seg += 1

signal.signal(signal.SIGHUP, p_1_handler)
signal.signal(signal.SIGINT, p_1_handler)
signal.signal(signal.SIGQUIT, p_1_handler)
signal.signal(signal.SIGILL, p_1_handler)
signal.signal(signal.SIGTRAP, p_1_handler)
signal.signal(signal.SIGABRT, p_1_handler)
signal.signal(signal.SIGBUS, p_1_handler)
signal.signal(signal.SIGFPE, p_1_handler)
signal.signal(signal.SIGUSR1, p_1_handler)
signal.signal(signal.SIGSEGV, p_1_handler)
signal.signal(signal.SIGUSR2, p_1_handler)
signal.signal(signal.SIGPIPE, p_1_handler)
signal.signal(signal.SIGTERM, p_1_handler)
signal.signal(signal.SIGALRM, p_1_handler)

def pollard_p_1(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int):

    """
    calculating primes number less than 100000
    """
    primes = [prime for prime in range(100000) if is_prime(prime)]


    B = isqrt(n)

    exp = []

    for prime in primes:
        for _ in range(floor(log(B, prime), bits=1024)):
            exp.append(prime)

    print("[+] Start pollard p-1 factorization")
    
    x = 1

    p, q = None, None

    for k in exp:
        x = Integer(x * k)
        g = gcd(Integer(pow(2, x, n))-1, n)
        if g > 1 and g < n:
            p, q = g, n//g
    

    if not p:
        print("[-] pollard p-1 factorization failed\n")
        sys.exit(1) # exit (failure)
    
    print("[+] pollard p-1 factorization complete\n")
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

    pollard_p_1(n, e, private, output_private, ciphertext_file, output_file, ciphertext)
    