#!/usr/local/bin/sage --python

##
#   Common factor attack
#   https://www.slideshare.net/VineetKumar130/common-factor-attack-on-rsa
##

from sage.all import gcd, inverse_mod, Integer

import os
import sys
import signal

"""
common factor's custom signal handler
"""

def fermat_handler(sigNum: int, frame: str) -> None:
    print("\n[-] common factor attack failed\n")
    sys.exit(1) # exit (failure)

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

LEGEND = """LEGEND:
n1: first modulous
e1: public exponent of first modulous
index: index of the first modulous
n2: second modulous
e2: public exponent of the second modulous
index: index of the second modulous
p: common factor
q1: other factor of n1
q2: other factor of n2

private key file from n1 and e1 (if output-dir is not specified)

private key file from n2 and e2 (if output-dir is not specified)

---------------------------------- press any key to continue"""

def common_factor(n: list, e: list, private: bool, output_dir: str) -> None:

    print("[+] common factor attack started")

    results = []

    j = 0

    while n:

        """
        pop public key values from n and e lists
        """
        tmp_n = n.pop(0)
        tmp_e = e.pop(0)

        """
        try to compute gcd with all the others values on the list
        """
        for i in range(len(n)):
            G = gcd(tmp_n, n[i])
            if G != 1:
                newres = {'n1': tmp_n, 'in1': str(j), 'e1': tmp_e, 'n2': n[i], 'in2': str(i+j+1), 'e2': e[i], 'p': int(G), 'q1': int(tmp_n//G), 'q2': int(n[i]//G)}
                results.append(newres)
        j += 1

    if not results:
        print("[-] common factor attack failed\n")
        sys.exit(1) # exit (success)
    
    print("[+] common factor attack complete\n")

    """
    move PWD in the parent path
    """
    pathname = os.path.dirname(sys.argv[0])
    abspath = os.path.abspath(pathname)
    os.chdir(abspath + "/../")

    """
    Print results
    """

    print(LEGEND, end = "")

    input()

    for res in results:
        print(f"""
n1: {res['n1']}
e1: {res['e1']}
index: {res['in1']}
n2: {res['n2']}
e2: {res['in2']}
index: {res['in2']}
p: {res['p']}
q1: {res['q1']}
q2: {res['q2']}
""")

        if private:
            try:
                if not output_dir:
                    os.system("sage --python -c 'from misc.software_path import *; import sys; sys.path.append(SOFTWARE_PATH); from pem_utils.certs_manipulation import *; create_privkey(" + str(res["n1"]) + ", " + str(res["e1"]) +", None, " + str(res["p"]) + ", " + str(res["q1"]) + ", " + "\"" + "None" + "\"" + ", \"PEM\")'")
                    os.system("sage --python -c 'from misc.software_path import *; import sys; sys.path.append(SOFTWARE_PATH); from pem_utils.certs_manipulation import *; create_privkey(" + str(res["n2"]) + ", " + str(res["e2"]) +", None, " + str(res["p"]) + ", " + str(res["q2"]) + ", " + "\"" + "None" + "\"" + ", \"PEM\")'")
                else:
                    os.system("sage --python -c 'from misc.software_path import *; import sys; sys.path.append(SOFTWARE_PATH); from pem_utils.certs_manipulation import *; create_privkey(" + str(res["n1"]) + ", " + str(res["e1"]) +", None, " + str(res["p"]) + ", " + str(res["q1"]) + ", " + "\"" + output_dir + "private_" + str(res["in1"]) + ".pem" + "\"" + ", \"PEM\")'")
                    os.system("sage --python -c 'from misc.software_path import *; import sys; sys.path.append(SOFTWARE_PATH); from pem_utils.certs_manipulation import *; create_privkey(" + str(res["n2"]) + ", " + str(res["e2"]) +", None, " + str(res["p"]) + ", " + str(res["q2"]) + ", " + "\"" + output_dir + "private_" + str(res["in2"]) + ".pem" + "\"" + ", \"PEM\")'")
            except OSError:
                print("[-] common factor attack -- OSError raised while constructing private key files")
                sys.exit(1) # exit (failure)
        print("----------------------------------\n")

    sys.exit(0) # exit (success)


if __name__ == "__main__":

    """
    parse the arguments correctly
    """
    n = [Integer(x) for x in sys.argv[1].split(":") if x]
    e = [Integer(x) for x in sys.argv[2].split(":") if x]

    assert len(n) == len(e)

    private = (sys.argv[3] == "True")
    output_dir = (None if sys.argv[4] == "None" else sys.argv[4])

    if output_dir:
        if output_dir[-1] != "/":
            output_dir += "/"

    if len(n) <= 1:
        print("\n[-] Too few values for common_factor attack\n")
        sys.exit(1) # exit (failure)

    common_factor(n, e, private, output_dir)
