#!/usr/local/bin/sage

##
# mersenne primes attack
##

import os
import sys
import signal

"""
mersenne primes custom signal handler
"""

def mersenne_handler(sigNum: int, frame: str) -> None:
    print("\n[-] mersenne attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, mersenne_handler)
signal.signal(signal.SIGINT, mersenne_handler)
signal.signal(signal.SIGQUIT, mersenne_handler)
signal.signal(signal.SIGILL, mersenne_handler)
signal.signal(signal.SIGTRAP, mersenne_handler)
signal.signal(signal.SIGABRT, mersenne_handler)
signal.signal(signal.SIGBUS, mersenne_handler)
signal.signal(signal.SIGFPE, mersenne_handler)
signal.signal(signal.SIGUSR1, mersenne_handler)
signal.signal(signal.SIGSEGV, mersenne_handler)
signal.signal(signal.SIGUSR2, mersenne_handler)
signal.signal(signal.SIGPIPE, mersenne_handler)
signal.signal(signal.SIGTERM, mersenne_handler)
signal.signal(signal.SIGALRM, mersenne_handler)

def mersenne(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:

    print("[+] Start mersenne attack")

    p, q = None, None

    primes = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20336011, 20996011, 24036583, 25964951, 30402457, 32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933]
    
    for prime in primes:
        if n % prime == 0:
            p = prime
            q = n//prime

    if not p:
        print("[-] mersenne attack failed\n")
        sys.exit(1) # exit (failure)
    
    print("[+] mersenne attack complete\n")
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
    n = int(sys.argv[1])
    e = int(sys.argv[2])
    private = (sys.argv[3] == "True")
    output_private = (None if sys.argv[4] == "None" else sys.argv[4])
    ciphertext_file = (None if sys.argv[5] == "None" else sys.argv[5])
    output_file = sys.argv[6]
    ciphertext = (None if sys.argv[7] == "None" else sys.argv[7])

    mersenne(n, e, private, output_private, ciphertext_file, output_file, ciphertext)