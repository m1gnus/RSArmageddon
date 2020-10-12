import sys

from binascii import hexlify
from functools import partial
from contextlib import redirect_stdout

from crypto import cipher, uncipher

from args import get_args
from utils import byte_length, output_cleartext

def run():
    args = get_args()

    if args.csubp == "cipher":
        f = partial(cipher, n=args.n, e=args.e, padding=args.padding)
    else:
        f = partial(uncipher, n=args.n, e=args.e, d=args.d, padding=args.padding)

    for text, filename in args.inputs:
        output = f(text)
        output_cleartext(output, filename, json_output=args.json)
