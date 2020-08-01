import sys
import subprocess
import binascii

from os import system

from gmpy2 import invert
from Crypto.PublicKey import RSA

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
            if base > 10: # invalid base
                raise ValueError("cannot use base > 9")
            return int(string, base) # valid base
    except ValueError as e:
        print("args_filter.py:int_filter ->",e)
        sys.exit(1)

"""
Takes a string in the format string[:base] and return the corresponding integer
"""
def wrap_int_filter(string: str) -> int:

    if not string:
        return None
    if isinstance(string, int):
        return string

    parameters = [x for x in string.split(":") if x]
    
    if len(parameters) > 1: # there is a base
        return int_filter(parameters[0], parameters[1])
    else:
        return int_filter(parameters[0])

"""
Takes a string in the format string:type and return the corresponding plaintext int
"""
def plaintext_filter(string: str) -> int:
    
    try:
        parameters = [x for x in string.split(":") if x]
        
        if len(parameters) > 1: # there is a type
            type_ = parameters[1]
        else:
            type_ = "str"
        
        plaintext = parameters[0]
    
        if type_ == "str":
            plaintext = int_filter("0x" + binascii.hexlify(plaintext.encode()).decode())
        elif type_ == "dec":
            plaintext = int_filter(plaintext, 10)
        elif type_ == "hex":
            plaintext = int_filter(plaintext) if len(plaintext) > 1 and plaintext[:2] == "0x" else int_filter("0x" + plaintext)
        elif type_ == "oct":
            plaintext = int_filter(plaintext, 8)
        elif type_ == "bin":
            plaintext = int_filter(plaintext) if len(plaintext) > 1 and plaintext[:2] == "0b" else int_filter(plaintext, 2)
        else:
            raise ValueError("Unknown type: " + type_)
        
        return plaintext
    except ValueError as e:
        print("args_filter.py:plaintext_filter ->", e)
        sys.exit(1)

"""
Takes a string in the format string:type and return the corresponding plaintext int
"""
def ciphertext_filter(string: str) -> int:
    
    try:
        parameters = [x for x in string.split(":") if x]
        
        if len(parameters) > 1: # there is a type
            type_ = parameters[1]
        else:
            type_ = "dec"
        
        plaintext = parameters[0]
    
        if type_ == "dec":
            plaintext = int_filter(plaintext, 10)
        elif type_ == "hex":
            plaintext = int_filter(plaintext) if len(plaintext) > 1 and plaintext[:2] == "0x" else int_filter("0x" + plaintext)
        elif type_ == "oct":
            plaintext = int_filter(plaintext, 8)
        elif type_ == "bin":
            plaintext = int_filter(plaintext) if len(plaintext) > 1 and plaintext[:2] == "0b" else int_filter(plaintext, 2)
        else:
            raise ValueError("Unknown type: " + type_)
        
        return plaintext
    except ValueError as e:
        print("args_filter.py:ciphertext_filter ->", e)
        sys.exit(1)

"""
Takes a list of arguments divided by comma (,) example1,example2,......
"""
def list_filter(string: str) -> list:
    
    parameters = [x for x in string.split(",") if x] if string else None

    return parameters

"""
Takes a path to a file containing lines in the form n:e and extract n and e values
"""
def recover_pubkey_value_from_file(path: str) -> list:

    try:
        parameters = [x.strip() for x in open(path, "r").readlines() if x]
    except OSError as e:
        print("args_filter.py:recover_pubkey_value_form_file ->", e)
        sys.exit(1)

    n = []
    e = []

    for line in parameters:
        parts = [x for x in line.split(":") if x]

        if len(parts) < 2:
            parts.append('65537')

        n.append(wrap_int_filter(parts[0]))
        e.append(wrap_int_filter(parts[1]))
    
    return n, e

"""
Takes a list of folders which contain public keys and extract values
"""
def recover_pubkey_value_from_folder(path: str, ext: str) -> list:

    n = []
    e = []

    if path[-1] != '/':
        path += '/'

    if ext[0] == '.':
        ext = '.' + ext

    files = [x for x in subprocess.check_output(['ls', '-al', path]).decode().split('\n') if x]
    files = [x for x in [y for y in y.split(" ") if y][8] if len(x) > 3]

    # Find public keys in folder
    files = [x.strip() for x in files if (len(x) > len(ext) and x[-(len(ext)):] == ext)]

    print("Importing Public Keys:")
    print('\n'.join(files))

    for file_ in files:
        vals = dump_values_from_key(file_)
        n.append(wrap_int_filter(vals[0]))
        e.append(wrap_int_filter(vals[1]))
    
    return n, e

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
Takes a modulous and check its consistency: this is the only "validate" function that has a return value,
because of its nature the management of the result is left to the programmer
"""
def validate_modulous(n: int) -> bool:

    res = [True, "[-]"]
    
    if n%2 == 0:
        res[0] = False
        res[1] += "--modulous is not odd--"
    if n<2:
        res[0] = False
        res[1] += "--modulous has to be >= 2--"
    
    if res[1] != "[-]":
        print(res[1])
    return res[0]

"""
Takes a string and check if its a valid argument for padding
"""
def validate_padding(arg: str) -> str:
    
    if arg == 'pkcs7' or arg == 'iso7816' or arg == 'x923':
        return arg
    else:
        return '' 

"""
Takes a string and check if its a valid argument for filepadding
"""
def validate_padding_for_file(arg: str) ->str:

    if arg == 'pkcs' or arg == 'oaep' or arg == 'raw' or arg == 'ssl':
        return arg
    else:
        return 'pkcs'

"""
Takes string which represent an integer and check if its valid for being a timer
"""
def validate_timer(time: str) -> int:
    if not time:
        tmp = 0
    else:
        tmp = wrap_int_filter(time)
        if tmp < 0:
            tmp = 0
    return tmp

"""
Takes a path and check if the key is a public key
"""
def validate_pubkey(path: str) -> None:
    
    try:
        if RSA.importKey(open(path, "rb").read()).has_private():
            raise Exception("The inserted key is a private key")
    except Exception as e:
        print("args_filter.py:validate_pubkey ->", e)
        sys.exit(1)

"""
Takes a path and check if the key is a private key
"""
def validate_privkey(path: str) -> None:
    
    try:
        if not RSA.importKey(open(path, "rb").read()).has_private():
            raise Exception("The inserted key is a public key")
    except Exception as e:
        print("args_filter.py:validate_privkey ->", e)
        sys.exit(1)

"""
Takes a number and check if its prime or not
"""
def check_prime(p: int) -> bool:

    if system("features/sage_isprime.sage " + str(p) + " 1>/dev/null") == 0:
        return False
    return True

"""
recover all the needed arguments to create a private key from the given ones
"""
def fill_privkey_args(n: int, e: int, d: int, p: int, q: int) -> tuple:

    """
    check that the required arguments is setted
    """

    if not n and ((not p) or (not q)):
        print("[-] you have to provide n or both p and q")
        sys.exit(1)
    if n and ((not p) and (not q)):
        print("[-] if you provide n, you must provide also p or q")
        sys.exit(1)
    
    if not e and not d:
        print("[-] you have to provide e or d")
        sys.exit(1)

    if not n:
        n = p*q
    elif not p:
        p = n//q
    elif not q:
        q = n//p
    
    if n != p*q:
        print("[-] N is not p*q!")
        sys.exit(1)

    phi = (p-1)*(q-1)

    if not e:
        e = int(invert(d, phi))
    elif not d:
        d = int(invert(e, phi))
    
    return n, e, d, p, q
