import sys

from signal import Signals, signal
from functools import wraps


def get_args():
    _, ciphertext, *nes = tuple(sys.argv)
    nes = {(int(n), int(e)) for n, e in (ne.split(":") for ne in nes)}
    return ciphertext, nes


name = None

def set_name(attack_name):
    global name
    name = attack_name


def with_name_set(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if name is None:
            raise RuntimeError("Attacks must call set_name before using this function")
        return f(*args, **kwargs)
    return wrapper


@with_name_set
def success(*, cleartext=None, qs=None):
    if qs is not None:
        print(f"qs: {' '.join(map(str, qs))}")
    if cleartext is not None:
        print("cleartext:")
        sys.stdout.write(cleartext)
    print(f"[+] {name} attack succeeded", file=sys.stderr)
    sys.exit(0)


@with_name_set
def fail():
    print(f"[-] {name} attack failed", file=sys.stderr)
    sys.exit(1)


def info(s):
    print(f"[*] {s}" if s else "", file=sys.stderr)


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
        fail()
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
