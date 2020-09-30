import sys

from args import get_args
from certs import print_key, print_key_json, generate_key, encode_pubkey, encode_privkey, load_key
from utils import compute_extra_key_elements


def run() -> None:
    """Execute pem command
    """
    args = get_args()

    n, e, d, p, q = args.n, args.e, args.d, args.p, args.q

    if args.dumpvalues:
        dp, dq, pinv, qinv = compute_extra_key_elements(d, p, q)
        if args.json:
            print_key_json(n, e, d, p, q, dp, dq, pinv, qinv, file=sys.stdout)
        else:
            print_key(n, e, d, p, q, dp, dq, pinv, qinv, file=sys.stderr)

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