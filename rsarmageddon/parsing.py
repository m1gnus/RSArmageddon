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

import re
import sys
import binascii
import subprocess

from base64 import b64decode, b85decode
from pathlib import Path

from .crypto import standards
from .utils import DEFAULT_E


def parse_unsigned(s, base=None):
    """Convert to int raising ValueError on negative values

    Arguments:
    s -- string to convert

    Keyword arguments:
    base -- numeric base of the conversion
    """
    if base is not None:
        if base < 2:
            raise ValueError("base cannot be less than 2")
        ret = int(s, base)
    else:
        s = s.strip()
        if len(s) > 1 and not s[1].isalpha():
            s = s.lstrip("0")
        if not s:
            s = "0"
        ret = int(s, 0)
    if ret < 0:
        raise ValueError(f"'{ret}' is not unsigned")
    return ret


def parse_int_arg(s):
    """Take a string in the format number[:base] or any format
    recognized by python and return the corresponding integer

    Arguments:
    s -- string to convert
    """
    number, sep, base = s.rpartition(":")
    if not sep:
        number, base = base, number
    number = number.strip()
    base = base.strip()
    try:
        if base in ("b64", "base64"):
            return int.from_bytes(b64decode(number, validate=True), "big")
        elif base in ("b85", "base85"):
            return int.from_bytes(b85decode(number), "big")
    except binascii.Error as e:
        raise ValueError(str(e)) from e

    if base:
        return parse_unsigned(number, int(base))
    else:
        return parse_unsigned(number)


time_re1 = re.compile(r"(\d+)([hms]?)")
time_re2 = re.compile(r"(?:(?:(\d+):)?(?:(\d+):))?(\d+)")
time_mult = {
    "": 1,
    "s": 1,
    "m": 60,
    "h": 3600
}
def parse_time(s):
    sc = s.strip().casefold()
    m1 = time_re1.fullmatch(sc)
    if m1:
        return int(m1.group(1)) * time_mult[m1.group(2)]
    m2 = time_re2.fullmatch(sc)
    if m2:
        h, m, s = m2.groups()
        h = h or "0"
        m = m or "0"
        h, m, s = int(h), int(m), int(s)
        return h*3600 + m*60 + s
    raise ValueError(f"Bad time '{s}'")


def parse_list(s):
    """Parse a comma separated list of arguments (example1,example2,...) into a list

    Arguments:
    s -- comma separated string
    """
    return [x if x else None for x in s.split(",")] if s else []


def parse_int_list(s):
    """Parse a comma separated list of ints (example1,example2,...) into a list

    Arguments:
    s -- comma separated string
    """
    return [parse_int_arg(x) if x is not None else None for x in parse_list(s)]


def parse_std_list(s):
    all_standards = ["raw", *standards.keys()]
    allowed = {*all_standards, "all"}
    l = [x.strip().casefold() for x in s.split(",") if x.strip()]
    l = list(dict.fromkeys(l)) # Deduplicate list keeping order
    for std in l:
        if std not in allowed:
            raise ValueError(f"Invalid encryption standard '{std}'")
    if "all" in l:
        l = all_standards
    return l


def path_or_stdout(s):
    if s == "-":
        return True
    return Path(s)


def parse_n_e_file(filename):
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n, _, e = line.partition(",")
            yield (parse_int_arg(n), parse_int_arg(e) if e else DEFAULT_E)
