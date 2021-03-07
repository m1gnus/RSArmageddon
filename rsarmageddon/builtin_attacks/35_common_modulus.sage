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
#   Common Modulus
##

import attack

ciphertexts, keys = attack.init("Common modulus", "common_modulus", min_keys=2, min_ciphertexts=2, deduplicate="keys")
n1, e1, _ = keys[0]
n2, e2, _ = keys[1]
c1, name = ciphertexts[0]
c2, _ = ciphertexts[1]

if n1 != n2:
    attack.fail("n1 and n2 have to be the same")

n = n1

if gcd(e1, e2) != 1:
    attack.fail("e1 and e2 are not coprime")

_, u, v = xgcd(e1, e2)

m = (pow(c1, u, n) * pow(c2, v, n)) % n

attack.cleartexts((m, name))
attack.success()
