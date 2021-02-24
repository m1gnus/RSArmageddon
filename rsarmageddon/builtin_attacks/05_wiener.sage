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
#   Wiener_Factorization_attack
#   https://en.wikipedia.org/wiki/Wiener%27s_attack
##

import attack

_, keys = attack.init("Wiener factorization", "wiener")
n, e, _ = keys[0]

n = Integer(n)
e = Integer(e)

cf_convergents = continued_fraction(e/n).convergents()

for el in cf_convergents:
    k = Integer(el.numerator())
    d = Integer(el.denominator())

    if k == 0 or (e*d - 1) % k != 0:
        continue

    phi = (e*d - 1)//k
    s = n - phi + 1
    delta = s*s - 4*n

    # If delta >= 0 then we have 2 real solutions
    if (delta < 0
            or not delta.is_integer()
            or not delta.is_square()
            or is_odd(s + isqrt(delta))):
        continue

    x = var('x')
    roots = solve(x**2 - s*x + n, x)
    p = roots[0].rhs()
    q = roots[1].rhs()

    if p < 0 or q < 0:
        continue

    if p * q == n:
        attack.keys((n, e, None, p, q))
        attack.success()

attack.fail()
