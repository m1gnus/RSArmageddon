import sys

from functools import wraps
from itertools import islice


name = None


def init(attack_name):
    global name
    name = attack_name
    print("[+] {} attack started".format(name), file=sys.stderr)


def with_name_set(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if name is None:
            raise RuntimeError("Attacks must call set_name before using this function")
        return f(*args, **kwargs)
    return wrapper


@with_name_set
def success(keys=(), cleartexts=()):
    for key in keys:
        if not isinstance(key, (tuple, list)) or len(key) not in (5, 6):
            raise ValueError("Bad key '{}'".format(key))
        if len(key) == 5:
            if len(keys) > 1:
                raise ValueError("Name is not optional for multiple keys")
            key = *key, None
        print("key: {}".format(",".join(str(x) if x is not None else "" for x in key)))
    for cleartext in cleartexts:
        if not isinstance(cleartext, int):
            raise ValueError("Bad cleartext '{}'".format(cleartext))
        print("cleartext: {}".format(cleartext))
    print("[+] {} attack succeeded".format(name), file=sys.stderr)
    sys.exit(0)


@with_name_set
def fail(s=None):
    if s is not None:
        print("[-] {}".format(s), file=sys.stderr)
    print("[-] {} attack failed".format(name), file=sys.stderr)
    sys.exit(1)


@with_name_set
def info(s=None):
    print("[*] {}".format(s) if s not in (None, "") else "", file=sys.stderr)


@with_name_set
def get_args(*, min_keys=1, deduplicate=False):
    ciphertexts = []
    keys = []
    for arg in islice(sys.argv, 1, None):
        lhs, sep, rhs = arg.partition(":")
        if sep:
            keys.append((int(lhs), int(rhs)))
        else:
            ciphertexts.append(int(lhs))
    if deduplicate:
        keys = list(dict.fromkeys(keys))
        if len(keys) < min_keys:
            fail("This attack needs at least {} distinct keys".format(min_keys))
    else:
        if len(keys) < min_keys:
            fail("This attack needs at least {} keys".format(min_keys))
    return ciphertexts, keys


_input = input
@with_name_set
def input(prompt=None, *, default=None, validator=None):
    if prompt is not None:
        prompt_default = ' [{}]'.format(default) if default is not None else ''
        prompt = "[+] {}{}: ".format(prompt, prompt_default)
    else:
        prompt = ""

    if validator is None:
        validator = lambda x: x

    while True:
        try:
            inp = _input(prompt).strip()
        except EOFError:
            if prompt:
                print(file=sys.stderr)
            fail()

        if not inp:
            if default is not None:
                return default
            else:
                print("[*] Must enter a value", file=sys.stderr)
                continue

        try:
            inp = validator(inp)
        except ValueError as e:
            print("[*] Invalid input ({})".format(e), file=sys.stderr)
        else:
            return inp
