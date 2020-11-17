import sys

from pathlib import Path
from functools import partial

from args import args
from crypto import cipher, uncipher
from utils import int_from_path, output_text, compute_d, compute_n, compute_pubkey, complete_privkey


def run():
    if args.command == "encrypt":
        n, e = compute_pubkey(args.n, args.e, args.d, args.p, args.q, args.phi)
        f = partial(cipher, n=n, e=e, padding=args.encryption_standard)
    else:
        d = compute_d(args.n, args.e, args.d, args.p, args.q, args.phi)
        n = compute_n(args.n, args.e, args.d, args.p, args.q, args.phi)
        f = partial(uncipher, n=n, e=args.e, d=d, padding=args.encryption_standard)

    if not args.inputs:
        print("Nothing to do", file=sys.stderr)

    for text, filename in args.inputs:
        if isinstance(text, Path):
            text = int_from_path(text)
        elif isinstance(text, bytes):
            text = int.from_bytes(text)
        output = f(text)
        encoding = None
        if args.command == "decrypt":
            encoding = args.encoding
        output_text(output, filename, encoding=encoding, json_output=args.json)
