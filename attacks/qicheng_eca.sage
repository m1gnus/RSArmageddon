#!/usr/local/bin/sage

##
# Qicheng general purpose factorization algorithm - https://www.cs.ou.edu/~qcheng/paper/speint.pdf
# script taken from https://github.com/Ganapati/RsaCtfTool/blob/master/sage/qicheng.sage
##

import sys
import os
import signal

sys.setrecursionlimit(Integer(1e5))

"""
qicheng's factorization custom signal handler
"""

def qicheng_handler(sigNum: int, frame: str) -> None:
    print("\n[-] Qicheng factorization failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, qicheng_handler)
signal.signal(signal.SIGINT, qicheng_handler)
signal.signal(signal.SIGQUIT, qicheng_handler)
signal.signal(signal.SIGILL, qicheng_handler)
signal.signal(signal.SIGTRAP, qicheng_handler)
signal.signal(signal.SIGABRT, qicheng_handler)
signal.signal(signal.SIGBUS, qicheng_handler)
signal.signal(signal.SIGFPE, qicheng_handler)
signal.signal(signal.SIGUSR1, qicheng_handler)
signal.signal(signal.SIGSEGV, qicheng_handler)
signal.signal(signal.SIGUSR2, qicheng_handler)
signal.signal(signal.SIGPIPE, qicheng_handler)
signal.signal(signal.SIGTERM, qicheng_handler)
signal.signal(signal.SIGALRM, qicheng_handler)

def qicheng_factorization(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:
    
    print("[+] Qicheng factorization started")

    R = Integers(n)
    attempts = 20
    js = [0, (-2^5)^3, (-2^5*3)^3, (-2^5*3*5*11)^3, (-2^6*3*5*23*29)^3]

    p, q = None, None

    for _ in range(attempts):

        for j in js:
            if j == 0:
                a = R.random_element()
                E = EllipticCurve([0, a])

            else:
                a = R(j)/(R(1728)-R(j))
                c = R.random_element()
                E = EllipticCurve([3*a*c^2, 2*a*c^3])

            x = R.random_element()
            z = E.division_polynomial(n, x)
            g = gcd(z, n)
            if g > 1:
                p = Integer(g)
                q = Integer(n)//p
                break
        
        if p:
            break
    
    if not p:
        print("[-] Qicheng factorization failed\n")
        sys.exit(1) # exit (failure)
    
    print("[+] Qicheng factorization complete\n")
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

    qicheng_factorization(n, e, private, output_private, ciphertext_file, output_file, ciphertext)