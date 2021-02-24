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
# Novelty Primes - Most numbers in the form 31(3*)7 are prime numbers
##

import attack
from attack import positive_int

_, keys = attack.init("Novelty primes factorization", "novelty")
n, e, _ = keys[0]

bound = attack.input("Insert upper bound: max number of digits", default=1000000, validator=positive_int)
bound = min(bound, floor(log(n, 10)+1))

for i in range(bound-4):
    p = int("313{}7".format("3"*i))
    q, r = divmod(n, p)
    if not r:
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
