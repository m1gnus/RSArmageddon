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
# mersenne primes attack
##

import attack


_, keys = attack.init("Mersenne primes factorization", "mersenne")
n, e, _ = keys[0]

primes = [
    2, 3, 5, 7, 13,
    17, 19, 31, 61, 89,
    107, 127, 521, 607, 1279,
    2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701,
    23209, 44497, 86243, 110503, 132049,
    216091, 756839, 859433, 1257787, 1398269,
    2976221, 3021377, 6972593, 13466917, 20336011,
    20996011, 24036583, 25964951, 30402457, 32582657,
    37156667, 42643801, 43112609, 57885161, 74207281,
    77232917, 82589933
]

for prime in primes:
    if n % prime == 0:
        p = prime
        q = n//prime
        break
else:
    attack.fail()

attack.keys((n, e, None, p, q))
attack.success()
