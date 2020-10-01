import sys

from functools import wraps


name = None


def init(attack_name):
    global name
    name = attack_name
    print(f"[+] {name} attack started", file=sys.stderr)


def with_name_set(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if name is None:
            raise RuntimeError("Attacks must call set_name before using this function")
        return f(*args, **kwargs)
    return wrapper


@with_name_set
def success(*keys, cleartext=None):
    for key in keys:
        print(f"key: {','.join(str(x) if x is not None else '' for x in key)}")
    if cleartext is not None:
        print("cleartext:")
        sys.stdout.write(cleartext)
    print(f"[+] {name} attack succeeded", file=sys.stderr)
    sys.exit(0)


@with_name_set
def fail(s=None):
    if s is not None:
        print(f"[-] {s}", file=sys.stderr)
    print(f"[-] {name} attack failed", file=sys.stderr)
    sys.exit(1)


@with_name_set
def info(s=None):
    print(f"[*] {s}" if s not in (None, "") else "", file=sys.stderr)


@with_name_set
def get_args(*, min_keys=1, deduplicate=False):
    _, ciphertext, *keys = tuple(sys.argv)
    keys = ((int(n), int(e)) for n, e in (ne.split(",") for ne in keys))
    if deduplicate:
        keys_deduplicated = list(dict.fromkeys(keys))
        if len(keys_deduplicated) < min_keys:
            fail("{name} attack needs at least {min_keys} distinct (n, e) pairs")
        return ciphertext, keys_deduplicated
    else:
        if len(keys) < min_keys:
            fail("{name} attack needs at least {min_keys} (n, e) pairs")
        return ciphertext, keys


_input = input
@with_name_set
def input(prompt=None, *, default=None, validator=None):
    if prompt is not None:
        prompt = f"[+] {prompt}{f' [{default}]' if default is not None else ''}: "
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
                print(f"[*] Must enter a value", file=sys.stderr)
                continue

        try:
            inp = validator(inp)
        except ValueError as e:
            print(f"[*] Invalid input ({e})", file=sys.stderr)
        else:
            return inp
