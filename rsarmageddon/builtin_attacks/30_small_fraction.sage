#!/usr/bin/env sage

##########################################################################
# RSArmageddon - RSA cryptography and cryptoanalysis toolkit             #
# Copyright (C) 2020,2021                                                #
# Vittorio Mignini a.k.a. M1gnus <vittorio.mignini@gmail.com>            #
# Simone Cimarelli a.k.a. Aquilairreale <aquilairreale@ymail.com>        #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

##
# small fraction attack (p/q close to a small fraction) - from https://github.com/Ganapati/RsaCtfTool/blob/master/sage/smallfraction.sage
##

import attack
from attack import positive_int

_, keys = attack.init("Small fraction factorization", "small_fraction")
n, e, _ = keys[0]

depth = attack.input("Insert depth", default=50, validator=positive_int)

x = PolynomialRing(Zmod(n), "x").gen()

p, q = None, None

for den in IntegerRange(2, depth+1):
    for num in IntegerRange(1, den):
        if gcd(num, den) != 1:
            continue

        r = den / num
        phint = isqrt(n * r)
        f = x - phint
        sr = f.small_roots(beta=0.5)

        if len(sr) <= 0:
            continue

        p = (phint - sr[0]).lift()
        if n % p == 0:
            q = n // p
            attack.keys((n, e, None, p, q))
            attack.success()

attack.fail()
