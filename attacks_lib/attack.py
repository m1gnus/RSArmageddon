import sys

from signal import Signals, signal
from functools import wraps


name = None


def set_name(attack_name):
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
def get_args(*, min_nes=1):
    _, ciphertext, *nes = tuple(sys.argv)
    nes = ((int(n), int(e)) for n, e in (ne.split(",") for ne in nes))
    nes_deduplicated = list(dict.fromkeys(nes))
    if len(nes_deduplicated) < min_nes:
        fail("Not enough N,E pairs")
    return ciphertext, nes_deduplicated


HANDLED_SIGNALS = {
    Signals.SIGABRT, Signals.SIGALRM, Signals.SIGBUS,
    Signals.SIGFPE,  Signals.SIGHUP,  Signals.SIGILL,
    Signals.SIGINT,  Signals.SIGPIPE, Signals.SIGQUIT,
    Signals.SIGSEGV, Signals.SIGTERM, Signals.SIGTRAP,
    Signals.SIGUSR1, Signals.SIGUSR2
}


def fail_on_signals(signals=HANDLED_SIGNALS):
    def handler(sig, frame):
        print(file=sys.stderr)
        fail(f"Caught termination signal {sig.name}")
    for s in signals:
        signal(s, handler)


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
