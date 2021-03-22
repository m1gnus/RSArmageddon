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
import signal
import multiprocessing

from operator import itemgetter
from functools import wraps
from itertools import count, islice
from contextlib import redirect_stdout

import output


name = None
_default_key_name = None


def init(attack_name, default_key_name, *, min_keys=1, min_ciphertexts=0, deduplicate=None):
    global name, _default_key_name

    name = attack_name
    _default_key_name = default_key_name

    def excepthook(exctype, value, traceback):
        if exctype in (KeyboardInterrupt, RuntimeError):
            sys.exit(2)
        else:
            sys.__excepthook__(exctype, value, traceback)
    sys.excepthook = excepthook

    ciphertexts = []
    keys = []
    color = "auto"

    with open(sys.argv[1], "r", encoding="ascii") as f:
        for line in f:
            line = line.strip()
            if not line or line.isspace():
                continue
            kind, _, line = line.partition(":")
            if kind == "k":
                n, e, keyname = line.split(",", maxsplit=2)
                keys.append((int(n), int(e), keyname or None))
            elif kind == "c":
                text, textname = line.split(",", maxsplit=1)
                ciphertexts.append((int(text), textname))
            elif kind == "C":
                color = line.strip()
            else:
                raise ValueError("Unexpected input type '{}' from input file".input(kind))

    output.init(color)

    if deduplicate:
        if deduplicate in ("n", "ns"):
            cmp_key = itemgetter(0)
        elif deduplicate == "keys":
            cmp_key = itemgetter(0, 1)
        else:
            raise ValueError("Bad value for deduplicate argument '{}'".format(deduplicate))
        keys = {cmp_key(key): key for key in reversed(keys)}
        keys = list(keys.values())
        keys.reverse()
        if len(keys) < min_keys:
            fail("This attack needs at least {} distinct keys".format(min_keys))
    else:
        if len(keys) < min_keys:
            fail("This attack needs at least {} keys".format(min_keys))

    if len(ciphertexts) < min_ciphertexts:
        fail("This attack needs at least {} ciphertexts".format(min_ciphertexts))

    output.success("{} attack started".format(name))
    return ciphertexts, keys


@wraps(multiprocessing.Pool)
def Pool(*args, **kwargs):
    old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = multiprocessing.Pool(*args, **kwargs)
    signal.signal(signal.SIGINT, old_handler)
    return pool


def with_name_set(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if name is None:
            raise RuntimeError("Attacks must call set_name before using this function")
        return f(*args, **kwargs)
    return wrapper


_keys = []
@with_name_set
def keys(*keys):
    _keys.extend(keys)
    for _, _, d, p, q, *_ in keys:
        for name, value in (("d", d), ("p", p), ("q", q)):
            if value is not None:
                info("{}: {}".format(name, value))


_cleartexts = []
@with_name_set
def cleartexts(*cleartexts):
    _cleartexts.extend(cleartexts)


@with_name_set
def success():
    unnamed_keys = sum(1 for key in _keys if len(key) == 5 or key[-1] is None)
    field_width = len(str(unnamed_keys))
    auto_name = (f"{_default_key_name}_{c:0{field_width}}" for c in count())
    for key in _keys:
        if not isinstance(key, (tuple, list)) or len(key) not in (5, 6):
            raise ValueError("Bad key '{}'".format(key))
        if len(key) == 5 or key[-1] is None:
            key = (*key[:5], next(auto_name))
        print("k:{}".format(",".join(str(x) if x is not None else "" for x in key)))
    for cleartext in _cleartexts:
        if isinstance(cleartext, int):
            text, textname = str(cleartext), ""
        elif isinstance(cleartext, tuple):
            text, textname = cleartext
            text = str(text)
            textname = textname if textname is not None else ""
        else:
            raise ValueError("Bad cleartext '{}'".format(cleartext))
        print("c:{},{}".format(text, textname))
    output.success("{} attack succeeded".format(name))
    sys.exit(0)


@with_name_set
def fail(*s, bad_key=False):
    if s:
        output.error(" ".join(map(str, s)))
    output.error("{} attack failed".format(name))
    sys.exit(1 if not bad_key else 2)


@with_name_set
def info(*s):
    if s:
        output.primary(" ".join(map(str, s)))
    else:
        output.newline()


def positive_int(s):
    i = int(s)
    if i <= 0:
        raise ValueError("Must be a positive number")
    return i


_input = input
@with_name_set
def input(prompt=None, *, default=None, validator=None):
    if prompt is not None:
        prompt_default = " [{}]".format(default) if default is not None else ""
        prompt = "{}{}: ".format(prompt, prompt_default)

    if validator is None:
        validator = lambda x: x

    while True:
        if prompt is not None:
            output.info(prompt, newline=False)

        try:
            inp = _input().strip()
        except EOFError:
            if prompt:
                output.newline()
            fail()

        if not inp:
            if default is not None:
                return default
            else:
                output.warning("Must enter a value")
                continue

        try:
            inp = validator(inp)
        except ValueError as e:
            output.warning("Invalid input ({})".format(e))
        else:
            return inp
