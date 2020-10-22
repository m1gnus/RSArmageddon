import os
import sys

from shutil import copyfileobj
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from importlib import resources
from contextlib import redirect_stdout
from subprocess import TimeoutExpired

import sage
import attack_lib
from args import args
from utils import to_bytes_auto, output_text, complete_privkey
from certs import encode_privkey
from crypto import uncipher
from attacks import attack_path


def parse_output(s):
    cleartexts = []
    keys = []
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        kind, _, value = map(str.strip, line.partition(":"))
        if kind == "c":
            text, _, file = value.partition(",")
            cleartexts.append((int(text), Path(file) if file else True))
        elif kind == "k":
            *key, name = value.split(",")
            key = tuple(int(x) if x else None for x in key)
            keys.append((key, name or None))
        else:
            raise ValueError(f"Unexpected return type '{kind}' from sage script")
    return cleartexts, keys


def run():
    args = get_args()

    with TemporaryDirectory() as attack_lib_dir, \
            NamedTemporaryFile("w", encoding="ascii") as input_file:
        with redirect_stdout(input_file):
            for (n, e), name in args.pubkeys:
                print(f"k:{n},{e},{name if name is not None else ''}")
            for text, name in args.ciphertexts:
                print(f"c:{text},{name if name is not True else ''}")
        input_file.flush()
        with resources.open_binary(attack_lib, "attack.py") as src, \
                open(Path(attack_lib_dir)/"attack.py", "wb") as dst:
            copyfileobj(src, dst)

        _, cyg_runtime = sage.get_sage()

        env = os.environ.copy()
        env["PYTHONPATH"] = str(sage.cyg_path(attack_lib_dir, cyg_runtime))

        for attack in args.attacks:
            try:
                script_manager = attack_path(attack)
            except ValueError as e:
                print(e, file=sys.stderr)
                continue

            with script_manager as script:
                try:
                    p = sage.run(script, input_file.name, env=env, timeout=args.timeout)
                except TimeoutExpired:
                    print(f"[W] Timeout expired for attack {attack}", file=sys.stderr)
                    continue

                if p.returncode == 2: # attack determined the key is bad (i.e. not an RSA key)
                    break

                if p.returncode: # attack failed for other reasons
                    continue

                cleartexts, keys = parse_output(p.stdout)

                if cleartexts:
                    print("[@] Cleartexts recovered", file=sys.stderr)
                    for text, file in cleartexts:
                        output_text(text, file, json_output=args.json)

                if len(keys) == 1:
                    key, _ = keys[0]
                    _, _, d, _, _ = key
                    if d is None:
                        key = complete_privkey(*key)

                    if args.output_private is True:
                        sys.stdout.buffer.write(encode_privkey(*key, "PEM"))
                        print()
                    elif args.output_private:
                        with open(args.output_private, "wb") as f:
                            f.write(encode_privkey(*key, "PEM"))

                    for text, filename in args.ciphertexts:
                        text_bytes = to_bytes_auto(text)
                        print(f"[$] Decrypting 0x{text_bytes.hex()}", file=sys.stderr)
                        n, e, d, _, _ = key
                        cleartext = uncipher(text, n, e, d, args.padding)
                        output_text(cleartext, filename, json_output=args.json)

                if args.output_dir is not None:
                    for key, name in keys:
                        key = complete_privkey(*key)
                        with open(args.output_dir/f"{name}.pem", "wb") as f:
                            f.write(encode_privkey(*key, "PEM"))

                if keys:
                    break
