#!/usr/bin/env sage

##
# small fraction attack (p/q cloe to a small fraction) - from https://github.com/Ganapati/RsaCtfTool/blob/master/sage/smallfraction.sage
##

import os
import sys
import signal

"""
small fraction custom signal handler
"""

def smallfraction_handler(sigNum: int, frame: str) -> None:
    print("\n[-] smallfraction attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, smallfraction_handler)
signal.signal(signal.SIGINT, smallfraction_handler)
signal.signal(signal.SIGQUIT, smallfraction_handler)
signal.signal(signal.SIGILL, smallfraction_handler)
signal.signal(signal.SIGTRAP, smallfraction_handler)
signal.signal(signal.SIGABRT, smallfraction_handler)
signal.signal(signal.SIGBUS, smallfraction_handler)
signal.signal(signal.SIGFPE, smallfraction_handler)
signal.signal(signal.SIGUSR1, smallfraction_handler)
signal.signal(signal.SIGSEGV, smallfraction_handler)
signal.signal(signal.SIGUSR2, smallfraction_handler)
signal.signal(signal.SIGPIPE, smallfraction_handler)
signal.signal(signal.SIGTERM, smallfraction_handler)
signal.signal(signal.SIGALRM, smallfraction_handler)

def smallfraction(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:

    print("[+] Start smallfraction attack")

    depth = input("[+] Insert depth (Integer value) (default 50): ")
    try: 
        depth = int(depth)
        print()
    except ValueError:
        print("[-] Invalid Value, default is setted\n")
        depth = 50

    x = PolynomialRing(Zmod(n), "x").gen()

    p, q = None, None

    for den in IntegerRange(2, depth + 1):
        for num in IntegerRange(1, den):
            if gcd(num, den) == 1:
                r = den / num
                phint = isqrt(n * r)
                f = x - phint
                sr = f.small_roots(beta=0.5)

                if len(sr) > 0:
                    p = phint - sr[0]
                    p = p.lift()
                    if n % p == 0:
                        q = n // p
                        assert(p*q == n)

    if not p:
        print("[-] small fraction attack failed\n")
        sys.exit(1) # exit (failure)
    
    print("[+] smallfraction attack complete\n")
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

    smallfraction(n, e, private, output_private, ciphertext_file, output_file, ciphertext)