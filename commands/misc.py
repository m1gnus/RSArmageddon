import os
import sys
import subprocess
import colorama

from importlib import resources
from tempfile import TemporaryDirectory

import sage
import scripts
import utils

from args import args
from utils import copy_resource, copy_resource_tree


def run():
    script_names = {
        "eulerphi": "euler_phi.sage",
        "factor":   "factor.sage",
        "ecm":      "ecm_factor.sage",
        "isprime":  "isprime.sage"
    }

    script_name = script_names[args.command]

    with resources.path(scripts, script_name) as script, \
            TemporaryDirectory() as attack_lib_dir:
        copy_resource(utils, "output.py", attack_lib_dir)
        copy_resource_tree(colorama, attack_lib_dir)

        _, cyg_runtime = sage.get_sage()

        env = os.environ.copy()
        env["PYTHONPATH"] = str(sage.cyg_path(attack_lib_dir, cyg_runtime))

        sage.run(script, str(args.n), env=env)
