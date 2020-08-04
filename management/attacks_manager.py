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

"""
pid of the attack process
"""
attack_pid = 0

"""
kill the actual attack process
"""
def terminate_attack(signalNumber: int, frame: str) -> None:

    global attack_pid

    if attack_pid != 0:
        os.kill(attack_pid, signal_)

"""
set terminate_attack as handler for SIGALRM
"""
signal.signal(signal.SIGALRM, terminate_attack)

def attack_manager(args: object) -> None:

    global attack_pid
    global pids

    """
    list of implemented attacks
    """
    attacks = {
        "fermat": {
            "pkey": "single", # single: requires only one couple of public key values, multi: requires more than one couple of public key values
            "scriptname": "fermat.sage"
        },
        "wiener": {
            "pkey": "single",
            "scriptname": "wiener.sage"
        },
        "p_1": {
            "pkey": "single",
            "scriptname": "pollard_p_1.sage"
        },
        "factordb": {
            "pkey": "single",
            "scriptname": "factordb.py"
        },
        "common_factor": {
            "pkey": "multi",
            "scriptname": "common_factor.sage"
        }
    }

    check_required(args.attacks)

    selected_attacks = list_filter(args.attacks)

    """
    take public key values from arguments
    """
    n = []
    e = []

    if args.n:
        n += [wrap_int_filter(x) for x in list_filter(args.n)]
        """
        if len(n) > len(e) then the missing e will be set to 65537 by default
        """
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

    if not n:
        print("[-] you have to insert at least one value for n")
        sys.exit(1)

    if "all" in selected_attacks:
        selected_attacks = list(attacks.keys())

    for attack in selected_attacks:
        if attack not in attacks.keys(): # invalid attack selected
            print("[Warning]: Invalid attack selected ->", attack)
            selected_attacks.remove(attack)
            continue
        else:
            attributes = attacks[attack]

        args_list = []

        if attributes["pkey"] == "single": # pass only the first couple of public key values to the attack script
            args_list.append(n[0])
            args_list.append(e[0])
        elif attributes["pkey"] == "multi": # pass the entire list of public key values to the attack script
            args_list += [":".join(n)] + [":".join(e)]

        args_list += [str(args.private)]

        ciphertext = (ciphertext_filter(args.ciphertext) if args.ciphertext else None)

        if attributes["pkey"] == "single":
            args_list += [args.output_private, args.ciphertext_file, args.output_file, ciphertext]
        elif attributes["pkey"] == "multi":
            args_list += [args.output_dir]
        
        """
        Transform None in "None"
        """
        args_list = [str(x) for x in args_list]

        """
        start the timer
        """
        signal.alarm(timer)

        p = subprocess.Popen([SOFTWARE_PATH + "/attacks/" + attributes["scriptname"]] + args_list)
        attack_pid = p.pid
        pids.append(attack_pid)
        res = p.wait()
        pids.remove(attack_pid)
        """
        reset the timer
        """
        signal.alarm(0)

        if res == 0: # success, private key recovered
            break