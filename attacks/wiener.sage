#!/usr/local/bin/sage --python

##
#   Wiener_Factorization_attack
#   https://en.wikipedia.org/wiki/Wiener%27s_attack
##

from sage.all import continued_fraction, solve, var, isqrt, Integer

import sys
import os
import signal

"""
wiener attack's custom signal handler
"""

def wiener_handler(sigNum: int, frame: str) -> None:
    print("\n[-] Wiener attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, wiener_handler)
signal.signal(signal.SIGINT, wiener_handler)
signal.signal(signal.SIGQUIT, wiener_handler)
signal.signal(signal.SIGILL, wiener_handler)
signal.signal(signal.SIGTRAP, wiener_handler)
signal.signal(signal.SIGABRT, wiener_handler)
signal.signal(signal.SIGBUS, wiener_handler)
signal.signal(signal.SIGFPE, wiener_handler)
signal.signal(signal.SIGUSR1, wiener_handler)
signal.signal(signal.SIGSEGV, wiener_handler)
signal.signal(signal.SIGUSR2, wiener_handler)
signal.signal(signal.SIGPIPE, wiener_handler)
signal.signal(signal.SIGTERM, wiener_handler)
signal.signal(signal.SIGALRM, wiener_handler)

"""
Take a number and return -1 if its not a perfect square, else return the square root
"""
def is_perfect_square(n: int) -> int:

    """
    equivalent to h = n%16
    """
    h = n & 0xF

    """
    the only accepted values for n%16 are 0,1,4,9: If modulo is not one of this values, then the number is not a perfect square
    """
    valid_values = [0, 1, 4, 9]

    if h in valid_values:

        """
        if h is in valid_values then is possible that n is a perfect square
        """
        t = isqrt(n)
        if t * t == n:
            return t
        else:
            return -1
    
    return -1

def wiener_factorization(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:

    print("[+] Start Wiener attack")

    cf_expansion = continued_fraction(e/n)
    w = continued_fraction(e/n)
    cf_convergents = cf_expansion.convergents()

    p = None
    q = None


    for el in cf_convergents:
        k = Integer(el.numerator())
        d = Integer(el.denominator())

        if k != 0 and (e * d - 1) % k == 0:
            phi = (e*d - 1)//k
            s = n - phi + 1
            delta = s*s - 4*n
            """
            If delta >= 0 then we have 2 real solutions
            """
            if delta >= 0:
                t = is_perfect_square(delta)
                """
                If delta is a perfect square and (b + sqrt(delta)) is even then the solutions is integer numbers
                """
                if t != -1 and (s + t) % 2 == 0:
                    x = var('x')
                    roots = solve(x**2 - s*x + n, x)
                    p_ = roots[0].rhs()
                    q_ = roots[1].rhs()
                    if p_ < 0 or q_ < 0:
                        continue
                    if p_*q_ == n:
                        p = p_
                        q = q_
                        break

    if not p or not q:
        print("[-] Wiener attack failed\n")
    else:
        print("[+] Wiener attack complete\n")
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

    wiener_factorization(n, e, private, output_private, ciphertext_file, output_file, ciphertext)
