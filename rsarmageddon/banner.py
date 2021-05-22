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

from encodings.aliases import aliases
from contextlib import redirect_stdout

from . import attacks
from .utils import output


banner_text = r"""
  ______  _____  ___                                      _     _
  | ___ \/  ___|/ _ \                                    | |   | |
  | |_/ /\ `--./ /_\ \_ __ _ __ ___   __ _  __ _  ___  __| | __| | ___  _ __
  |    /  `--. \  _  | '__| '_ ` _ \ / _` |/ _` |/ _ \/ _` |/ _` |/ _ \| '_ \
  | |\ \ /\__/ / | | | |  | | | | | | (_| | (_| |  __/ (_| | (_| | (_) | | | |
  \_| \_|\____/\_| |_/_|  |_| |_| |_|\__,_|\__, |\___|\__,_|\__,_|\___/|_| |_|
                                            __/ |
                                           |___/

  Written by M1gnus && AquilaIrreale -- PGIATASTI

"""

credits_text = """\
  Glory to PGiatasti:
      - Vittorio aka M1gnus
      - Alessio aka Alexius
      - Cristiano aka ReverseBrain
      - Riccardo aka ODGrip
      - Nalin aka Lotus
      - Emanuele aka KaiserSource
      - Federico aka Heichou
      - Antonio aka CoffeeStraw
      - Giacomo aka Giaxo
      - Alessandro aka ale100gs
      - Simone aka AquilaIrreale

  https://pgiatasti.it/ -- Visit our site to find out more about us
"""


def print_banner():
    output.yellow(banner_text)


def print_credits():
    output.white(credits_text)


def print_attacks_short():
    all_attacks = set(attacks.builtin)
    all_attacks.update(attacks.installed)
    for attack in sorted(all_attacks):
        print(attack)


def _print_attacks(header, attacks):
    output.white(f" {header} ".center(32, "="))
    output.white(f"==={str(len(attacks)).center(26)}===")
    output.white("="*32)
    print()

    for attack in sorted(attacks):
        output.white(attack)


def print_attacks():
    with redirect_stdout(sys.stderr):
        _print_attacks("Builtin", attacks.builtin)
        if attacks.installed:
            print()
            _print_attacks("Installed", attacks.installed)
        print()


def print_encodings():
    for enc in sorted(c for c in set(aliases.values()) if not c.endswith("_codec")):
        print(enc)


def version(version, codename):
    print(f"RSArmageddon v{version} --{codename}--")
