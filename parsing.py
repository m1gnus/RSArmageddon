import sys
import binascii
import subprocess

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
    """Take a string in the format string[:base] and return the corresponding integer

    Arguments:
    s -- string to convert
    """
    args = [x for x in s.split(":") if x]
    if len(args) == 2:
        args[1] = int(args[1])
    if len(args) > 2:
        raise ValueError(f"Too many ':' in '{s}'")
    return parse_unsigned(*args)


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
