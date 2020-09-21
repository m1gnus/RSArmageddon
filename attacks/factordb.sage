#!/usr/bin/env sage

##
#   FactorDB factorization
#   http://factordb.com/
##

import requests
from bs4 import BeautifulSoup as bsoup

from gmpy2 import invert

import sys
import os
import signal

import binascii

"""
factordb factorization custom signal handler
"""

def factordb_handler(sigNum: int, frame: str) -> None:
    print("\n[-] factordb factorization failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, factordb_handler)
signal.signal(signal.SIGINT, factordb_handler)
signal.signal(signal.SIGQUIT, factordb_handler)
signal.signal(signal.SIGILL, factordb_handler)
signal.signal(signal.SIGTRAP, factordb_handler)
signal.signal(signal.SIGABRT, factordb_handler)
signal.signal(signal.SIGBUS, factordb_handler)
signal.signal(signal.SIGFPE, factordb_handler)
signal.signal(signal.SIGUSR1, factordb_handler)
signal.signal(signal.SIGSEGV, factordb_handler)
signal.signal(signal.SIGUSR2, factordb_handler)
signal.signal(signal.SIGPIPE, factordb_handler)
signal.signal(signal.SIGTERM, factordb_handler)
signal.signal(signal.SIGALRM, factordb_handler)

URL = "http://factordb.com/index.php"

def factor_db(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> tuple:
    
    print("[+] factordb factorization started")

    """
    build the payload correctly
    """
    payload = f"?query={n}"

    """
    make the request and create bsoup object
    """
    r = requests.get(URL+payload)
    soup = bsoup(r.text, features="lxml")

    """
    http://factordb.com/status.html
    """
    if soup.find_all("table")[1].find_all("td")[4].text != 'FF':
        p, q = None, None
        print("factordb factorization failed\n")
        sys.exit(1) # exit (failure)
    
    p, q = None, None

    """
    recover p and q
    """
    p_link = "http://factordb.com/" + soup.find_all("a")[11].get("href", "")
    q_link = "http://factordb.com/" + soup.find_all("a")[12].get("href", "")

    soup_p = bsoup(requests.get(p_link).text, features="lxml")
    p_link = "http://factordb.com/" + (soup_p.find_all("td")[12].findChild().get("href", ""))
    soup_p = bsoup(requests.get(p_link).text, features="lxml")
    p = int(soup_p.find_all("td")[11].get_text().replace("\n", ""))

    if q_link != "http://factordb.com/":
        soup_q = bsoup(requests.get(q_link).text, features="lxml")
        q_link = "http://factordb.com/" + (soup_q.find_all("td")[12].findChild().get("href", ""))
        soup_q = bsoup(requests.get(q_link).text, features="lxml")
        q = int(soup_q.find_all("td")[11].get_text().replace("\n", ""))

    print("[+] factordb factorization complete\n")
    print("[*] p:", p)
    if q:
        print("[*] q:", q), "\n"
    else:
        print("\n[+] Detected prime power RSA:")
        i = 0
        n_ = n
        while n_ != 1:
            n_ //= p
            i += 1
        phi = (pow(p, i) - pow(p, i-1))
        d = int(invert(e, phi))
        print("[*] n   =", p, "^", i)
        print("[*] phi =", phi)
        print("[*] d   =", d)
        if ciphertext:
            print("\n[*] c:", ciphertext)
            m = pow(ciphertext, d, n)
            hexm = hex(m)
            rawm = binascii.unhexlify(hexm[2:])
            print("\n[*] Plaintext:")
            print("[*] dec:", m)
            print("[*] hex:", hexm)
            print("[*] raw:", rawm)
        sys.exit(0) # exit (success)

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
    ciphertext = (None if sys.argv[7] == "None" else int(sys.argv[7]))

    factor_db(n, e, private, output_private, ciphertext_file, output_file, ciphertext)
