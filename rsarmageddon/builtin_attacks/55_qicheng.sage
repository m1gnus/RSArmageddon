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
# Qicheng general purpose factorization algorithm - https://www.cs.ou.edu/~qcheng/paper/speint.pdf
# script taken from https://github.com/Ganapati/RsaCtfTool/blob/master/sage/qicheng.sage
##

import sys

# dangerous: may crash the interpreter
# no big deal since we are running in a subinterpreter
sys.setrecursionlimit(100000)

import attack

_, keys = attack.init("Qi Cheng factorization", "qicheng")
n, e, _ = keys[0]

ATTEMPTS = 20

R = Integers(n)
js = (0, (-2^5)^3, (-2^5*3)^3, (-2^5*3*5*11)^3, (-2^6*3*5*23*29)^3)
p, q = None, None

for j in js * ATTEMPTS:
    if not j:
        a = R.random_element()
        E = EllipticCurve([0, a])
    else:
        a = R(j)/(R(1728)-R(j))
        c = R.random_element()
        E = EllipticCurve([3*a*c^2, 2*a*c^3])

    x = R.random_element()
    z = E.division_polynomial(n, x)
    g = gcd(z, n)

    if g > 1:
        p = Integer(g)
        q = Integer(n)//p
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
