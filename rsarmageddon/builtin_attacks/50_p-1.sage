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
#   p-1 pollard
#   https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm
##

import attack

_, keys = attack.init("Pollard's p-1 factorization", "pollard_p_1")
n, e, _ = keys[0]

B = isqrt(n)

x = 1

for k in primes(10000):
    x *= k
    attack.info(x)
    p = gcd(power_mod(2, x, n)-1, n)
    if 2 < p < n:
        q = n//p
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
