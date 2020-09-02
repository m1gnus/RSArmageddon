#!/usr/local/bin/sage --python

##
# Novelty Primes - Most numbers in the form 31(3*)7 are prime numbers
##

#!/usr/local/bin/sage

##
# small factor attack
##

import os
import sys
import signal

"""
novelty primes custom signal handler
"""

def novelty_primes_handler(sigNum: int, frame: str) -> None:
    print("\n[-] novelty_primes attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, novelty_primes_handler)
signal.signal(signal.SIGINT, novelty_primes_handler)
signal.signal(signal.SIGQUIT, novelty_primes_handler)
signal.signal(signal.SIGILL, novelty_primes_handler)
signal.signal(signal.SIGTRAP, novelty_primes_handler)
signal.signal(signal.SIGABRT, novelty_primes_handler)
signal.signal(signal.SIGBUS, novelty_primes_handler)
signal.signal(signal.SIGFPE, novelty_primes_handler)
signal.signal(signal.SIGUSR1, novelty_primes_handler)
signal.signal(signal.SIGSEGV, novelty_primes_handler)
signal.signal(signal.SIGUSR2, novelty_primes_handler)
signal.signal(signal.SIGPIPE, novelty_primes_handler)
signal.signal(signal.SIGTERM, novelty_primes_handler)
signal.signal(signal.SIGALRM, novelty_primes_handler)

def novelty_primes(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:

    print("[+] Start novelty_primes attack")

    ubound = input("[+] Insert upper bound: max number of digits (Integer value) (default 25): ")
    try: 
        ubound = int(ubound)
        print()
    except ValueError:
        print("[-] Invalid Value, default is setted\n")
        ubound = 25

    p, q = None, None

    base = str(3137)
    while len(base) <= ubound:
        base = int("31" + "3" + base[2:])
        if n%base == 0:
            p = base
            q = n//base
            break
        base = str(base)
    
    if not p:
        print("[-] novelty_primes attack failed\n")
        sys.exit(1) # exit (failure)
    
    print("[+] novelty_primes attack complete\n")
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

    novelty_primes(n, e, private, output_private, ciphertext_file, output_file, ciphertext)