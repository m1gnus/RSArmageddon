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
import subprocess
import colorama

from importlib import resources
from tempfile import TemporaryDirectory

from .. import sage
from .. import scripts
from .. import utils

from ..args import args
from ..utils import copy_resource_module, copy_resource_tree


def run():
    script_names = {
        "eulerphi": "euler_phi.sage",
        "factor":   "factor.sage",
        "ecm":      "ecm_factor.sage",
        "isprime":  "isprime.sage"
    }

    script_name = script_names[args.command]

    with resources.path(scripts, script_name) as script, \
            TemporaryDirectory() as libs_dir:
        copy_resource_module(utils, "output", libs_dir)
        copy_resource_tree(colorama, libs_dir)

        _, cyg_runtime = sage.get_sage()

        env = os.environ.copy()
        env["PYTHONPATH"] = str(sage.cyg_path(libs_dir, cyg_runtime))

        sage.run(script, str(args.n), args.color, env=env)
