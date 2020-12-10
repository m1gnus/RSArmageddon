import sys
import attacks
import output

from encodings.aliases import aliases
from contextlib import redirect_stdout


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
      - Andrei aka S0uND_0f_s1lence
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


def version():
    print("RSArmageddon v2.0 --Ares--")
