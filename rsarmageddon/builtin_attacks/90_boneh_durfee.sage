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
#  Based on https://github.com/mimoo/RSA-and-LLL-attacks
##

import attack
from attack import positive_int

# Setting debug to true will display more informations
# about the lattice, the bounds, the vectors...
debug = False

# Setting strict to true will stop the algorithm (and
# return (-1, -1)) if we don't have a correct
# upperbound on the determinant. Note that this
# doesn't necesseraly mean that no solutions
# will be found since the theoretical upperbound is
# usualy far away from actual results. That is why
# you should probably use `strict = False`
strict = False

# This is experimental, but has provided remarkable results
# so far. It tries to reduce the lattice as much as it can
# while keeping its efficiency. I see no reason not to use
# this option, but if things don't work, you should try
# disabling it
helpful_only = True
dimension_min = 7 # stop removing if lattice reaches that dimension

# Increase precision in Sage's RealField
RR = RealField(20000)

# display stats on helpful vectors
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii,ii] >= modulus:
            nothelpful += 1

    attack.info(nothelpful, "/", BB.dimensions()[0], " vectors are not helpful")


# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = '{:02d} '.format(ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        attack.info(a)


# tries to remove unhelpful vectors
# we start at current = n-1 (last vector)
def remove_unhelpful(BB, monomials, bound, current):
    # end of our recursive function
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB

    # we start by checking from the end
    for ii in range(current, -1, -1):
        # if it is unhelpful:
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
            # let's check if it affects other vectors
            for jj in range(ii + 1, BB.dimensions()[0]):
                # if another vector is affected:
                # we increase the count
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj

            # level:0
            # if no other vectors end up affected
            # we remove it
            if affected_vectors == 0:
                attack.info("Removing unhelpful vector", ii)
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii-1)
                return BB

            # level:1
            # if just one was affected we check
            # if it is affecting someone else
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # if it is affecting even one vector
                    # we give up on this one
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # remove both it if no other vector was affected and
                # this helpful vector is not helpful enough
                # compared to our unhelpful one
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(bound - BB[ii, ii]):
                    attack.info("Removing unhelpful vectors", ii, "and", affected_vector_index)
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii-1)
                    return BB
    # nothing happened
    return BB


# Boneh and Durfee revisited by Herrmann and May
#
# finds a solution if:
# * d < N^delta
# * |x| < e^delta
# * |y| < e^0.5
# whenever delta < 1 - sqrt(2)/2 ~ 0.292
#
# Returns:
# * 0,0   if it fails
# * -1,-1 if `strict=true`, and determinant doesn't bound
# * x0,y0 the solutions of `pol`
def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    # substitution (Herrman and May)
    PR.<u, x, y> = PolynomialRing(ZZ)
    Q = PR.quotient(x*y + 1 - u) # u = xy + 1
    polZ = Q(pol).lift()

    UU = XX*YY + 1

    # x-shifts
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
            gg.append(xshift)
    gg.sort()

    # x-shifts list of monomials
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)
    monomials.sort()

    # y-shifts (selected by Herrman and May)
    for jj in range(1, tt + 1):
        for kk in range((mm//tt) * jj, mm + 1):
            yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift) # substitution

    # y-shifts list of monomials
    for jj in range(1, tt + 1):
        for kk in range((mm//tt) * jj, mm + 1):
            monomials.append(u^kk * y^jj)

    # construct lattice B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)

    # Prototype to reduce the lattice
    if helpful_only:
        # automatically remove
        BB = remove_unhelpful(BB, monomials, modulus^mm, nn-1)
        # reset dimension
        nn = BB.dimensions()[0]
        if nn == 0:
            return 0, 0

    # check if vectors are helpful
    if debug:
        helpful_vectors(BB, modulus^mm)

    # check if determinant is correctly bounded
    det = BB.det()
    bound = modulus^(mm*nn)
    if det >= bound:
        attack.info("We do not have det < bound. Solutions might not be found.")
        attack.info("Try with higher m and t.")
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            attack.info("size det(L) - size e^(m*n) = ", (diff))
        if strict:
            return -1, -1
    else:
        attack.info("det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)")

    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus^mm)

    # LLL
    if debug:
        attack.info("Optimizing basis of the lattice via LLL, this can take a long time")

    BB = BB.LLL()

    if debug:
        attack.info("LLL is done!")

    # transform vector i & j -> polynomials 1 & 2
    if debug:
        attack.info("Looking for independent vectors in the lattice")

    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
            # for i and j, create the two polynomials
            PR.<w,z> = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w*z+1,w,z) * BB[pol1_idx, jj] / monomials[jj](UU,XX,YY)
                pol2 += monomials[jj](w*z+1,w,z) * BB[pol2_idx, jj] / monomials[jj](UU,XX,YY)

            # resultant
            PR.<q> = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)

            # are these good polynomials?
            if rr.is_zero() or rr.monomials() == [1]:
                continue

            rr = rr(q, q)

            # solutions
            soly = rr.roots()

            if len(soly) == 0:
                attack.info("Your prediction (delta) is too small")
                return 0, 0

            soly = soly[0][0]
            ss = pol1(q, soly)
            solx = ss.roots()

            if len(solx) == 0 or solx[0][0] <= 0:
                continue

            solx = solx[0][0]
            return solx, soly

    attack.info("No independent vectors could be found. This should very rarely happen...")
    return 0, 0


_, keys = attack.init("Boneh-Durfee factorization", "boneh_durfee")
n, e, _ = keys[0]

def parse_delta(s):
    delta = float(s)
    if not 0.001 <= delta <= 0.292:
        raise ValueError("Must be between .001 and .292")
    return delta

# the hypothesis on the private exponent (the theoretical maximum is 0.292)
delta = attack.input("Insert hypotesis on private exponent (between 0.001 and 0.292)", validator=parse_delta, default=float(.18))

# you should tweak this (after a first run), (e.g. increment it until a solution is found)
m = attack.input("Insert size of lattice (bigger is better but slower)", validator=positive_int, default=4)

# you need to be a lattice master to tweak these
t = int((1-2*delta) * m)  # optimization from Herrmann and May
X = ((RR(n)^RR(delta))*RR(2)).integer_part() # this _might_ be too much
Y = (pow(RR(n),RR(1/2))).integer_part()   # correct if p, q are ~ same size

# Problem put in equation
P.<x,y> = PolynomialRing(ZZ)
A = int((n+1)/2)
pol = 1 + x * (A + y)

solx, soly = boneh_durfee(pol, e, m, t, X, Y)

# found a solution?
if solx > 0:
    d = int(pol(solx, soly) / e)
    attack.keys((n, e, d, None, None))
    attack.success()
else:
    attack.fail()
