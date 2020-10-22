import sys

from functools import wraps
from itertools import count, islice
from contextlib import redirect_stdout


def positive_int(s):
    i = int(s)
    if i <= 0:
        raise ValueError("Must be a positive number")
    return i


name = None
_default_key_name = None


def init(attack_name, default_key_name):
    global name, _default_key_name

    name = attack_name
    _default_key_name = default_key_name

    def excepthook(exctype, value, traceback):
        if exctype in (KeyboardInterrupt, RuntimeError):
            sys.exit(2)
        else:
            sys.__excepthook__(exctype, value, traceback)
    sys.excepthook = excepthook

    print("[+] {} attack started".format(name), file=sys.stderr)


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
    print("[+] {} attack succeeded".format(name), file=sys.stderr)
    sys.exit(0)


@with_name_set
def fail(*s, bad_key=False):
    if s:
        print("[-]", *map(str, s), file=sys.stderr)
    print("[-] {} attack failed".format(name), file=sys.stderr)
    sys.exit(1 if not bad_key else 2)


@with_name_set
def info(*s):
    if s:
        print("[*]", *map(str, s), file=sys.stderr)
    else:
        print(file=sys.stderr)


@with_name_set
def get_args(*, min_keys=1, min_ciphertexts=0, deduplicate=False):
    ciphertexts = []
    keys = []

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
            else:
                raise ValueError(f"Unexpected input type '{kind}' from input file")

    if deduplicate:
        keys = {tuple(key): keyname for *key, keyname in keys}
        keys = [(*key, keyname) for key, keyname in keys.items()]
        if len(keys) < min_keys:
            fail("This attack needs at least {} distinct keys".format(min_keys))
    else:
        if len(keys) < min_keys:
            fail("This attack needs at least {} keys".format(min_keys))

    if len(ciphertexts) < min_ciphertexts:
        fail("This attack needs at least {} cihertexts".format(min_cihertexts))

    return ciphertexts, keys


_input = input
@with_name_set
def input(prompt=None, *, default=None, validator=None):
    if prompt is not None:
        prompt_default = " [{}]".format(default) if default is not None else ""
        prompt = "[@] {}{}: ".format(prompt, prompt_default)
    else:
        prompt = ""

    if validator is None:
        validator = lambda x: x

    with redirect_stdout(sys.stderr):
        while True:
            try:
                inp = _input(prompt).strip()
            except EOFError:
                if prompt:
                    print()
                fail()

            if not inp:
                if default is not None:
                    return default
                else:
                    print("[*] Must enter a value")
                    continue

            try:
                inp = validator(inp)
            except ValueError as e:
                print("[*] Invalid input ({})".format(e))
            else:
                return inp
