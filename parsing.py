import sys
import binascii
import subprocess


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
    args = [x for x in string.split(":") if x]
    if len(args) == 2:
        args[1] = int(args[1])
    if len(args) > 2:
        raise ValueError(f"Too many ':' in '{s}'")
    parse_unsigned(*args)


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
    return [int(x) if x is not None else None for x in parse_list(s)]


def validate_padding(s: str) -> str:
    """Take a string and check if its a valid argument for padding

    Arguments:
    s -- padding
    """
    cs = s.casefold()
    if cs in {"pkcs7", "iso7816", "x923", None}:
        return cs
    else:
        raise ValueError(f"Invalid padding '{s}'")


def validate_file_padding(s: str) -> str:
    """Take a string and check if its a valid argument for file padding

    Arguments:
    s -- padding
    """
    cs = s.casefold()
    if cs in {"pkcs", "oaep", "raw", "ssl"}:
        return cs
    else:
        raise ValueError(f"Invalid file padding '{s}'")


def validate_file_format(s: str) -> str:
    """Take a string and check if its a valid argument for file format

    Arguments:
    s -- file format
    """
    cs = s.casefold()
    if cs.casefold() in {"pem", "der", "openssh"}:
        return cs
    else:
        raise ValueError(f"Invalid file format {s}")
