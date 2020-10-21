import sys

from functools import partial

from args import args
from crypto import cipher, uncipher
from utils import int_from_path, output_text


def run():
    if args.command == "encrypt":
        n, e = compute_pubkey(args.n, args.e, args.d, args.p, args.q, args.phi)
        f = partial(cipher, n=args.n, e=args.e, padding=args.encryption_standard)
    else:
        d = compute_d(args.n, args.e, args.d, args.p, args.q, args.phi)
        n = compute_n(args.n, args.e, args.d, args.p, args.q, args.phi)
        f = partial(uncipher, n=args.n, e=args.e, d=args.d, padding=args.encryption_standard)

    if not args.inputs:
        print("Nothing to do", file=sys.stderr)

    for text, filename in args.inputs:
        if isinstance(text, Path):
            text = int_from_path(text)
        elif isinstance(text, str):
            text = text.encode("ascii")
        output = f(text)
        output_text(output, filename, json_output=args.json)
