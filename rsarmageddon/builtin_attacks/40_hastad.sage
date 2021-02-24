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
# hastad broadcast attack - https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-Hastad-Broadcast
##

from itertools import combinations

import attack

ciphertexts, keys = attack.init("Hastad broadcast", "hastad", min_keys=2, min_ciphertexts=2, deduplicate="keys")
ns, es, _ = tuple(zip(*keys))
cs, _ = tuple(zip(*ciphertexts))
_, name = ciphertexts[0]

if len(ns) != len(cs):
    attack.fail("Number of ciphertexts and public keys differ")

if not len(set(es)) == 1:
    attack.fail("RSA exponents differ")

e = Integer(es[0])

if len(ns) > 20:
    attack.info("Too many messages, skipping safety pairwise GCD check, results may be inconsistent")
elif any(gcd(a, b) != 1 for a, b in combinations(ns, 2)):
    attack.fail("Public key moduli are not coprime")

cr = crt([Integer(c) for c in cs], [Integer(n) for n in ns])

try:
    m = cr.nth_root(e)
except ValueError:
    attack.fail()

attack.cleartexts((m, name))
attack.success()
