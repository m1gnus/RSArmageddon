import sys
import binascii
import subprocess

from pathlib import Path


def parse_unsigned(s: str, base=0) -> int:
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


def parse_int_arg(s: str) -> int:
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


def parse_list(s: str) -> list:
    """Parse a comma separated list of arguments (example1,example2,...) into a list

    Arguments:
    s -- comma separated string
    """
    return [x if x else None for x in s.split(",")] if s else []


def parse_int_list(s: str) -> list:
    """Parse a comma separated list of ints (example1,example2,...) into a list

    Arguments:
    s -- comma separated string
    """
    return [parse_int_arg(x) if x is not None else None for x in parse_list(s)]


def validate_padding(s: str) -> str:
    """Take a string and check if its a valid argument for file padding

    Arguments:
    s -- padding
    """
    cs = s.casefold()
    if cs in {"pkcs", "oaep", "raw"}:
        return cs
    else:
        raise ValueError(f"Invalid file padding '{s}'")


def validate_file_format(s: str) -> str:
    """Take a string and check if its a valid argument for file format

    Arguments:
    s -- file format
    """

    formats = {
        "pem": "PEM",
        "der": "DER",
        "openssh": "OpenSSH"
    }

    try:
        return formats[s.casefold()]
    except KeyError:
        raise ValueError(f"Invalid file format {s}")


def path_or_stdout(s: str) -> Path:
    if s == "-":
        return True
    return Path(s)
