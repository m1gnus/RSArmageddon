#!/usr/local/bin/sage

##
# small factor attack
##

import os
import sys
import signal

"""
small factor custom signal handler
"""

def smallfactor_handler(sigNum: int, frame: str) -> None:
    print("\n[-] smallfactor attack failed\n")
    sys.exit(1) # exit (failure)

signal.signal(signal.SIGHUP, smallfactor_handler)
signal.signal(signal.SIGINT, smallfactor_handler)
signal.signal(signal.SIGQUIT, smallfactor_handler)
signal.signal(signal.SIGILL, smallfactor_handler)
signal.signal(signal.SIGTRAP, smallfactor_handler)
signal.signal(signal.SIGABRT, smallfactor_handler)
signal.signal(signal.SIGBUS, smallfactor_handler)
signal.signal(signal.SIGFPE, smallfactor_handler)
signal.signal(signal.SIGUSR1, smallfactor_handler)
signal.signal(signal.SIGSEGV, smallfactor_handler)
signal.signal(signal.SIGUSR2, smallfactor_handler)
signal.signal(signal.SIGPIPE, smallfactor_handler)
signal.signal(signal.SIGTERM, smallfactor_handler)
signal.signal(signal.SIGALRM, smallfactor_handler)

def smallfactor(n: int, e: int, private: bool, output_private: str, ciphertext_file: str, output_file: str, ciphertext: int) -> None:

    print("[+] Start smallfactor attack")

    ubound = input("[+] Insert upper bound (Integer value) (default 100000): ")
    try: 
        ubound = int(ubound)
        print()
    except ValueError:
        print("[-] Invalid Value, default is setted\n")
        ubound = 100000

    p, q = None, None

    for i in range(2, ubound + 1):
        if n%i == 0:
            p = i
            q = n//i
    
    if not p:
        print("[-] smallfactor attack failed\n")
        sys.exit(1) # exit (failure)
    
    print("[+] smallfactor attack complete\n")
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

    smallfactor(n, e, private, output_private, ciphertext_file, output_file, ciphertext)