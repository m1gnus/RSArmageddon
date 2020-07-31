"""
attacks management
"""
import sys

from parsing.args_filter import *
from pem_utils.certs_manipulation import *

from misc.signal_handler import *
from misc.software_path import *

import time
import subprocess

attack_pid = 0

def terminate_attack(signalNumber: int, frame: str) -> None:

    global attack_pid

    if attack_pid != 0:
        os.kill(attack_pid, signal_)

signal.signal(signal.SIGALRM, terminate_attack) # signal.alarm(time: seconds)

def attack_manager(args: object) -> None:

    global attack_pid

    attacks = {
        'fermat': {
            'pkey': 'single',
            'scriptname': 'fermat.sage'
        },
        'wiener': {
            'pkey': 'single',
            'scriptname': 'wiener.sage'
        },
        'p_1': {
            'pkey': 'single',
            'scriptname': 'pollard_p_1.sage'
        },
        'factordb': {
            'pkey': 'single',
            'scriptname': 'factordb.py'
        },
        'common_factor': {
            'pkey': 'multi',
            'scriptname': 'common_factor.sage'
        }
    }

    n = []
    e = []

    check_required(args.attacks)

    selected_attacks = list_filter(args.attacks)

    if args.n:
        n += [wrap_int_filter(x) for x in list_filter(args.n)]
        e = [wrap_int_filter(x) for x in list_filter(args.e)] if args.e else []
        e += [65537] * (len(n) - len(e))
       
    if args.publickey:
        vals = dump_values_from_key(args.publickey)
        n.append(vals[0])
        e.append(vals[1])
    
    if args.publickey_dir:
        folders = [x for x in args.publickey_dir.split(",") if x]

        for folder in folders:
            vals = recover_pubkey_value_from_folder(folder, args.ext)
            n += vals[0]
            e += vals[1]
    
    if args.n_e_file:
        vals = recover_pubkey_value_from_file(args.n_e_file)
        n += vals[0]
        e += vals[1]

    timer = validate_timer(args.timeout)

    if 'all' in selected_attacks:
        selected_attacks = list(attacks.keys())

    for attack in selected_attacks:
        if attack not in attacks.keys():
            print("[Warning]: Invalid attack selected ->", attack)
            selected_attacks.remove(attack)
            continue
        else:
            attributes = attacks[attack]

        args_list = []

        if attributes['pkey'] == 'single':
            args_list.append(n[0])
            args_list.append(e[0])
        elif attributes['pkey'] == 'multi':
            args_list += [':'.join(n)] + [':'.join(e)]

        args_list += [str(args.private)]

        ciphertext = (ciphertext_filter(args.ciphertext) if args.ciphertext else None)

        if attributes['pkey'] == 'single':
            args_list += [args.output_private, args.ciphertext_file, args.output_file, ciphertext]
        elif attributes['pkey'] == 'multi':
            args_list += [args.output_dir]
            
        args_list = [str(x) for x in args_list]

        signal.alarm(timer)

        p = subprocess.Popen([SOFTWARE_PATH + "/attacks/" + attributes['scriptname']] + args_list)
        attack_pid = p.pid
        p.wait()

        signal.alarm(0)