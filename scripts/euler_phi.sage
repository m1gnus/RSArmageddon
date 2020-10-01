#!/usr/bin/env sage

import sys


n = Integer(sys.argv[1])
print("[+] Start calculating euler's phi of {}".format(n), file=sys.stderr)
res = euler_phi(n)
print("[*] {}".format(res), file=sys.stderr)
