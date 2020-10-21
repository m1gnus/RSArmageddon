import sys

from args import args
from certs import print_key, print_key_json, generate_key, encode_pubkey, encode_privkey, load_key
from utils import compute_extra_key_elements


def run() -> None:
    """Execute pem command
    """
    n, e, d, p, q = args.n, args.e, args.d, args.p, args.q

    if args.dump_values:
        dp, dq, pinv, qinv = compute_extra_key_elements(d, p, q)
        if args.json:
            print_key_json(n, e, d, p, q, dp, dq, pinv, qinv, file=sys.stdout)
        else:
            print_key(n, e, d, p, q, dp, dq, pinv, qinv, file=sys.stderr)

    if args.create_public:
        key = encode_pubkey(n, e, args.file_format)
        if args.create_public is True:
            sys.stdout.buffer.write(key)
            print()
        else:
            with open(args.create_public, "wb") as f:
                f.write(key)

    if args.create_private:
        key = encode_privkey(n, e, d, p, q, args.file_format)
        if args.create_private is True:
            sys.stdout.buffer.write(key)
            print()
        else:
            with open(args.create_private, "wb") as f:
                f.write(key)
