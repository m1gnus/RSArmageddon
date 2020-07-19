"""
Takes two parameters: string,base and return the integer value wich is represented by the string.
If base is None, the string will be converted to int by following the standards representations of
numbers in base 16,2,8,10.
"""
def int_filter(string: str, base) -> int:
    try:
        if not base:
            if string[:2] == '0x':
                return int(string[2:], 16)
            elif string[:2] == '0b':
                return int(string[2:], 2)
            elif string[0] == '0':
                return int(string[1:], 8)
            else:
                return int(string[2:], 10)
        else:
            return int(string, base)
    except ValueError as e:
        print("args_filter.py:int_filter",e)

