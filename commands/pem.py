import sys

from args import get_args
from certs import print_key, generate_key, encode_pubkey, encode_privkey, load_key
from utils import compute_extra_key_elements


def run() -> None:
    """Execute pem command
    """
    args = get_args()

    n, e, d, p, q = args.n, args.e, args.d, args.p, args.q

    if args.dumpvalues:
        print_key(n, e, d, p, q, *compute_extra_key_elements(d, p, q), file=sys.stderr)

    if args.cpub:
        key = encode_pubkey(n, e, args.format)
        if args.cpub is True:
            sys.stdout.buffer.write(key)
        else:
            with open(args.cpub, "wb") as f:
                f.write(key)

    if args.cpriv:
        key = encode_privkey(n, e, d, p, q, args.format)
        if args.cpriv is True:
            sys.stdout.buffer.write(key)
        else:
            with open(args.cpriv, "wb") as f:
                f.write(key)