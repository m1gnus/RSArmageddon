import sys
import json

from binascii import hexlify
from functools import partial
from contextlib import redirect_stdout

from crypto import cipher, uncipher

from args import get_args
from utils import byte_length

def run():
    args = get_args()

    if args.csubp == "cipher":
        f = partial(cipher, n=args.n, e=args.e, padding=args.padding)
    else:
        f = partial(uncipher, n=args.n, e=args.e, d=args.d, padding=args.padding)

    for text, filename in args.inputs:
        output = f(text)
        output_raw = output.to_bytes(byte_length(output), "big")
        if filename is True:
            output_hex = f"0x{hexlify(output_raw).decode('ascii')}"
            if args.json:
                json.dump({
                    "output": output,
                    "dec": str(output),
                    "hex": output_hex,
                    "raw": str(output_raw)
                }, sys.stdout, indent=4)
            else:
                with redirect_stdout(sys.stderr):
                    print(f"[+] ciphertext (dec): {output}")
                    print(f"[+] ciphertext (hex): {output_hex}")
                    print(f"[+] ciphertext (raw): {output_raw}")
                    print()
        else:
            with open(filename, "wb") as file:
                file.write(output_raw)