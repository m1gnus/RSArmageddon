#!/usr/bin/env sage

import sys
import output


n = Integer(sys.argv[1])
output.success("Start calculating euler's phi of {}".format(n))
res = euler_phi(n)
output.success("Done")
output.primary("{}".format(res))
