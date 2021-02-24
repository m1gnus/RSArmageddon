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
#   Common factor attack
#   https://www.slideshare.net/VineetKumar130/common-factor-attack-on-rsa
##

from itertools import combinations

import attack


def common_factor(indices):
    i, j = indices
    n1, e1, name1 = keys[i]
    n2, e2, name2 = keys[j]
    p = gcd(n1, n2)
    if p != 1:
        q1 = n1//p
        q2 = n2//p
        return n1, e1, n2, e2, p, q1, q2, name1, name2


_, keys = attack.init("Common factor", "common_factor", min_keys=2, deduplicate="ns")

found = False

with attack.Pool() as pool:
    indices = combinations(range(len(keys)), 2)
    for ret in pool.imap_unordered(common_factor, indices, chunksize=10000):
        if ret is not None:
            found = True
            n1, e1, n2, e2, p, q1, q2, name1, name2 = ret
            attack.keys(
                    (n1, e1, None, p, q1, name1),
                    (n2, e2, None, p, q2, name2))

if found:
    attack.success()
else:
    attack.fail()
