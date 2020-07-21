import sys
import subprocess

from os import system

"""
Takes two parameters: string,base and return the integer value wich is represented by the string.
If base is None, the string will be converted to int by following the standards representations of
numbers in base 16,2,8,10.
"""
def int_filter(string: str, base = '0') -> int:
    try:
        base = int(base)
        if base <= 0:
            if string[:2] == '0x': # hexadecimal
                return int(string[2:], 16)
            elif string[:2] == '0b': # binary
                return int(string[2:], 2)
            elif string[0] == '0': # octal
                return int(string[1:], 8)
            else:
                return int(string, 10) # decimal
        else:
            if base > 9: # invalid base
                raise ValueError("cannot use base > 9")
            return int(string, base) # valid base
    except ValueError as e:
        print("args_filter.py:int_filter ->",e)
        sys.exit(1)

"""
Takes a string in the format string[:base] and return the corresponding integer
"""
def wrap_int_filter(string: str) -> int:
    parameters = [x for x in string.split(":") if x]
    if len(parameters) > 1: # there is a base
        return int_filter(parameters[0], parameters[1])
    else:
        return int_filter(parameters[0])

"""
Takes an arbitrary number of args, if at least one of this args is None, then the function raise a ValueError exception
"""
def check_required(*nargs) -> None:
    try:
        for arg in nargs:
            if not arg:
                raise ValueError("One of the required arguments is not setted: " + ' '.join(list(nargs)))
    except ValueError as e:
        print("args_filter.py:check_required", e)
        sys.exit(1)

"""
Takes a modulous and check its consistency
"""
def validate_modulous(n: int) -> bool:
    res = [True, "[-]"]
    
    if n%2 == 0:
        res[0] = False
        res[1] += " modulous is not odd|"
    if n<2:
        res[0] = False
        res[1] += " modulous has to be >= 2|"
    
    if res[1] != "[-]":
        print(res[1])
    return res[0]

"""
Takes a number and check if its prime or not
"""
def check_prime(p: int) -> bool:
    if system("features/sage_isprime.sage " + str(p) + " 1>/dev/null") == 0:
        return False
    return True