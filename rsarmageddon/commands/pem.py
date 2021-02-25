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

import sys

from ..args import args
from ..utils import output
from ..certs import print_key, print_key_json, generate_key, encode_pubkey, encode_privkey, load_key
from ..utils import compute_extra_key_elements, compute_pubkey, complete_privkey


def run():
    if args.generate:
        n, e, d, p, q = generate_key()
    else:
        n, e, d, p, q = args.n, args.e, args.d, args.p, args.q

        try:
            n, e = compute_pubkey(n, e, d, p, q)
            n, e, d, p, q = complete_privkey(n, e, d, p, q)
        except ValueError:
            pass

    if args.dump_values:
        dp, dq, pinv, qinv = compute_extra_key_elements(d, p, q)
        if args.json:
            print_key_json(n, e, d, p, q, dp, dq, pinv, qinv)
        else:
            print_key(n, e, d, p, q, dp, dq, pinv, qinv)

    if args.create_public:
        key = encode_pubkey(n, e, args.file_format)
        if args.create_public is True:
            sys.stdout.buffer.write(key)
            print()
        else:
            with open(args.create_public, "wb") as f:
                f.write(key)

    if args.create_private:
        key = encode_privkey(n, e, d, p, q, args.file_format)
        if args.create_private is True:
            sys.stdout.buffer.write(key)
            print()
        else:
            with open(args.create_private, "wb") as f:
                f.write(key)

    if not any((args.dump_values, args.create_public, args.create_private)):
        output.error("Nothing to do")
