"""
management of general purpose features
"""
import sys
import subprocess
import os

from banner import credits, show_attacks, version
from parsing.args_filter import wrap_int_filter

from misc.signal_handler import *
from misc.software_path import *

def general_features_manager(args: object) -> None:
    
    global pids

    if args.n_phi: # --factor <int>
        int_input = wrap_int_filter(args.n_phi)
        p = subprocess.Popen([SOFTWARE_PATH + "/features/sage_euler_phi.sage", str(int_input)])
        pids.append(p.pid)
        p.wait()
        sys.exit(0)
    if args.tofactor: # --factor <int>
        int_input = wrap_int_filter(args.tofactor)
        p = subprocess.Popen([SOFTWARE_PATH + "/features/sage_factor.sage", str(int_input)])
        pids.append(p.pid)
        p.wait()
        sys.exit(0)
    if args.tofactorwecm: # --ecm <int>
        int_input = wrap_int_filter(args.tofactorwecm)
        p = subprocess.Popen([SOFTWARE_PATH + "/features/sage_ecm_factor.sage", str(int_input)])
        pids.append(p.pid)
        p.wait()
        sys.exit(0)
    if args.tofactorwqsieve: # --qsieve <int>
        int_input = wrap_int_filter(args.tofactorwqsieve)
        p = subprocess.Popen([SOFTWARE_PATH + "/features/sage_qsieve_factor.sage", str(int_input)])
        pids.append(p.pid)
        p.wait()
        sys.exit(0)
    if args.checkprime: # --isprime <int>
        int_input = wrap_int_filter(args.checkprime)
        p = subprocess.Popen([SOFTWARE_PATH + "/features/sage_isprime.sage", str(int_input)])
        pids.append(p.pid)
        p.wait()
        sys.exit(0)
    if args.showversion:
        version()
        sys.exit(0)
    if args.showcredits: # --credits
        credits()
        sys.exit(0)
    if args.showattacks: # --show-attacks
        show_attacks()
        sys.exit(0)
