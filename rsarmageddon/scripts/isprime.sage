#!/usr/bin/env sage

import sys
import output


n = Integer(sys.argv[1])
output.init(sys.argv[2])

output.success("Start Primality test")
if is_prime(n):
    output.info("The number is prime")
else:
    output.info("The number is not prime")
