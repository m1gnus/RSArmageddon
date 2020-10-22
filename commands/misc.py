import sys
import subprocess
import os

from importlib import resources

import sage
import scripts

from args import args


def run() -> None:
    script_names = {
        "eulerphi": "euler_phi.sage",
        "factor":   "factor.sage",
        "ecm":      "ecm_factor.sage",
        "isprime":  "isprime.sage"
    }

    script_name = script_names[args.command]
    with resources.path(scripts, script_name) as script:
        sage.run(script, str(args.n))
