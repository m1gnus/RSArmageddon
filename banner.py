import sys
import attacks

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

Written by M1gnus && Lotus -- Guest starring: AquilaIrreale -- PGIATASTI
"""

credits_text = """
Written by Vittorio aka M1gnus and Nalin aka L07u5
Guest starring Simone aka AquilaIrreale

Glory to PGiatasti:
    - Vittorio aka M1gnus
    - Alessio aka Alexius
    - Cristiano aka ReverseBrain
    - Riccardo aka ODGrip
    - Nalin aka Lotus
    - Emanuele aka KaiserSource
    - Federico aka Heichou
    - Antonio aka CoffeeStraw

https://pgiatasti.it/ -- -- Visit our site to discover more about us
"""


def print_banner():
    print(banner_text, file=sys.stderr)


def print_credits():
    print(credits_text, file=sys.stderr)


def print_attacks_short():
    all_attacks = set(attacks.builtin)
    all_attacks.update(attacks.installed)
    for attack in sorted(all_attacks):
        print(attack)


def _print_attacks(header, attacks):
    print(f" {header} ".center(32, "="))
    print(f"==={str(len(attacks)).center(26)}===")
    print("="*32)
    print()

    for attack in sorted(attacks):
        print(attack)


def print_attacks():
    with redirect_stdout(sys.stderr):
        print()
        _print_attacks("Builtin", attacks.builtin)
        if attacks.installed:
            print()
            _print_attacks("Installed", attacks.installed)
        print()


def version():
    print("RSArmageddon v.1.0 --Athena--")
