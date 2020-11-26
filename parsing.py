import sys
import binascii
import subprocess

from base64 import b64decode, b85decode
from pathlib import Path

from utils import DEFAULT_E


def parse_unsigned(s, base=0):
    """Convert to int raising ValueError on negative values

    Arguments:
    s -- string to convert

    Keyword arguments:
    base -- numeric base of the conversion
    """
    ret = int(s, base)
    if ret < 0:
        raise ValueError(f"'{ret}' is not unsigned")
    return ret


def parse_int_arg(s):
    """Take a string in the format number[:base] and return the corresponding integer

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
        base = int(base)
    else:
        base = 10

    return parse_unsigned(number, base)


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
