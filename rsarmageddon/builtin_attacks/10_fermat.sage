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
#   Fermat_factorizations
#   https://en.wikipedia.org/wiki/Fermat's_factorization_method
##


import attack

_, keys = attack.init("Fermat factorization", "fermat")
n, e, _ = keys[0]

a = isqrt(n)
b2 = a*a - n
b = a

while b*b != b2:
    a = a + 1
    b2 = a*a - n
    b = isqrt(b2)

p = a+b
q = a-b

if n != (p*q):
    attack.fail("n != p * q")

attack.keys((n, e, None, p, q))
attack.success()
