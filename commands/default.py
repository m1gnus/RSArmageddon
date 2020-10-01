import sys
import subprocess
import os

import scripts

from importlib import resources

from args import get_args

import sage

from banner import credits, show_attacks, version


def run() -> None:
    args = get_args()

    script_names = {
        "n_phi": "euler_phi.sage",
        "tofactor": "factor.sage",
        "tofactorwecm": "ecm_factor.sage",
        "checkprime": "isprime.sage",
    }

    try:
        action = next(k for k,v in vars(c).items() if v is not None)
    except StopIteration:
        return

    try:
        script_name = script_names[action]
    except KeyError:
        pass
    else:
        with resources.path(scripts, script_name) as script:
            sage.run(script, getattr(args, action))
        return

    if args.showversion:
        version()
    elif args.showcredits:
        credits()
    elif args.showattacks:
        show_attacks()
