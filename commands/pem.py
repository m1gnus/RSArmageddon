import sys

from args import args
from utils import output
from certs import print_key, print_key_json, generate_key, encode_pubkey, encode_privkey, load_key
from utils import compute_extra_key_elements, compute_pubkey, complete_privkey


def run():
    if args.generate:
        n, e, d, p, q = generate_key()
    else:
        n, e, d, p, q = args.n, args.e, args.d, args.p, args.q

        try:
            n, e = compute_pubkey(n, e, d, p, q)
            n, e, d, p, q = complete_privkey(n, e, d, p, q)
        except ValueError:
            pass

    if args.dump_values:
        dp, dq, pinv, qinv = compute_extra_key_elements(d, p, q)
        if args.json:
            print_key_json(n, e, d, p, q, dp, dq, pinv, qinv)
        else:
            print_key(n, e, d, p, q, dp, dq, pinv, qinv)

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

    if not any((args.dump_values, args.create_public, args.create_private)):
        output.error("Nothing to do")
