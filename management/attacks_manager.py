"""
attacks management
"""
import sys

from parsing.args_filter import *
from pem_utils.certs_manipulation import *

from misc.signal_handler import *

import time
import multiprocessing

def attack_manager(args: object) -> None:

    n = []
    e = []

    check_required(args.attacks)

    if args.n:
        n += [wrap_int_filter(x) for x in list_filter(args.n)]
        e_list = [wrap_int_filter(x) for x in list_filter(args.e)]
        e_list += [65537] * (len(n) - len(e_list))
       
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
    
