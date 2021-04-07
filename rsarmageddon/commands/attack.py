##########################################################################
# RSArmageddon - RSA cryptography and cryptoanalysis toolkit             #
# Copyright (C) 2020,2021                                                #
# Vittorio Mignini a.k.a. M1gnus <vittorio.mignini@gmail.com>            #
# Simone Cimarelli a.k.a. Aquilairreale <aquilairreale@ymail.com>        #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

import os
import sys
import colorama

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from itertools import chain
from contextlib import redirect_stdout
from subprocess import TimeoutExpired

from .. import sage
from .. import utils
from .. import attack_lib
from ..args import args
from ..certs import encode_privkey, load_key, load_keys
from ..crypto import uncipher
from ..attacks import attack_path, builtin, installed
from ..parsing import parse_n_e_file
from ..utils import (
        output, DEFAULT_E, to_bytes_auto, output_text,
        compute_d, complete_privkey, int_from_path,
        compute_d, copy_resource_module, copy_resource_tree)


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
    attacks = list(dict.fromkeys(args.attacks))
    if len(attacks) != len(args.attacks):
        output.warning("Attacks specified more than once are ignored")
    try:
        i = attacks.index("all")
    except ValueError:
        pass
    else:
        l = attacks[:i]
        r = attacks[i+1:]
        all_attacks = {
            **installed,
            **builtin
        }
        for attack in chain(l, r):
            all_attacks.pop(attack, None)
        attacks = [*l, *all_attacks, *r]

    keys = []
    for n, e in args.keys:
        if e is None:
            e = DEFAULT_E
        keys.append(((n, e), None))
    for path in args.n_e_files:
        keys.extend((key, None) for key in parse_n_e_file(path))
    for path in args.key_paths:
        if path.is_dir():
            keys.extend(load_keys(path, recursive=args.recursive, exts=args.exts))
        else:
            n, e, _, _, _ = load_key(path)
            keys.append(((n, e), path.name))

    if not keys:
        output.error("please provide at least one key")
        return

    with TemporaryDirectory() as attack_lib_dir, \
            NamedTemporaryFile("w", encoding="ascii") as input_file:
        with redirect_stdout(input_file):
            print(f"C:{args.color}")
            for (n, e), name in keys:
                print(f"k:{n},{e},{name if name is not None else ''}")
            for text, name in args.inputs:
                if isinstance(text, Path):
                    text = int_from_path(text)
                elif isinstance(text, bytes):
                    text = int.from_bytes(text, "big")
                print(f"c:{text},{name if name is not True else ''}")
        input_file.flush()

        copy_resource_module(attack_lib, "attack", attack_lib_dir)
        copy_resource_module(utils, "output", attack_lib_dir)
        copy_resource_tree(colorama, attack_lib_dir)

        _, cyg_runtime = sage.get_sage()

        env = os.environ.copy()
        env["PYTHONPATH"] = str(sage.cyg_path(attack_lib_dir, cyg_runtime))

        for attack in attacks:
            try:
                script_manager = attack_path(attack)
            except ValueError as e:
                output.error(e)
                continue

            with script_manager as script:
                try:
                    p, script_output = sage.run(script, input_file.name, env=env, timeout=args.timeout)
                except TimeoutExpired:
                    output.warning(f"Timeout expired for attack {attack}")
                    continue

                if p.returncode == 2: # attack determined the key is bad (i.e. not an RSA key)
                    break

                if p.returncode: # attack failed for other reasons
                    continue

                cleartexts, keys = parse_output(script_output)

                if cleartexts:
                    output.info("Plaintext recovered")
                    for text, file in cleartexts:
                        output_text("plaintext", text, file, encoding=args.encoding, json_output=args.json)
                        if file is True:
                            print()

                if len(keys) == 1:
                    key, _ = keys[0]
                    n, e, d, p, q = key
                    if d is None:
                        d = compute_d(*key)
                        key = (n, e, d, p, q)

                    if args.output_key_file is None and args.output_key:
                        args.output_key_file = True

                    if args.output_key_file is True:
                        sys.stdout.buffer.write(encode_privkey(*key, args.file_format))
                        print()
                    elif args.output_key_file:
                        with open(args.output_key_file, "wb") as f:
                            f.write(encode_privkey(*key, args.file_format))

                    for text, filename in args.inputs:
                        if isinstance(text, Path):
                            with open(text, "rb") as f:
                                text_bytes = f.read()
                                text = int.from_bytes(text_bytes, "big")
                        else:
                            text_bytes = to_bytes_auto(text)
                        for std in args.encryption_standard:
                            output.newline()
                            output.info(f"Decrypting 0x{text_bytes.hex()} with encryption standard {std}")
                            try:
                                cleartext = uncipher(text, n, e, d, std)
                            except ValueError as err:
                                output.error(err)
                            else:
                                output_text("plaintext", cleartext, filename, encoding=args.encoding, json_output=args.json)
                            if filename is True:
                                print()

                if args.output_key_dir is not None:
                    for key, name in keys:
                        key = complete_privkey(*key)
                        with open(args.output_key_dir/f"{name}.pem", "wb") as f:
                            f.write(encode_privkey(*key, "PEM"))

                if keys:
                    break
