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
import re
from pathlib import Path
from importlib import resources
from importlib.resources import contents, is_resource

from . import builtin_attacks


if os.name == "posix":
    try:
        cfg_dir = Path(os.environ["XDG_CONFIG_HOME"])
    except KeyError:
        cfg_dir = Path.home()/".config"
    user_atk_dir = cfg_dir/"rsarmageddon"/"attacks"
    user_atk_dir.mkdir(parents=True, exist_ok=True)
    sys_atk_dir = Path("/usr/share/rsarmageddon/attacks")
    path = [user_atk_dir, sys_atk_dir]
elif os.name == "nt":
    app_data = Path(os.environ.get("LOCALAPPDATA", os.environ["APPDATA"]))
    user_atk_dir = app_data/"RSArmageddon"/"attacks"
    user_atk_dir.mkdir(parents=True, exist_ok=True)
    path = [user_atk_dir]
else:
    path = []


suffix_re = re.compile(r"\.sage$")
prefix_re = re.compile(r"^\d{2}_")


def attack_name(s):
    if isinstance(s, Path):
        s = s.stem
    else:
        s = suffix_re.sub("", s)
    return prefix_re.sub("", s).replace("\n", " ")


builtin = {
    attack_name(res): res
    for res in sorted(contents(builtin_attacks))
    if is_resource(builtin_attacks, res)
        and res.endswith(".sage")
}


installed = {
    attack_name(f): f
    for d in reversed(path)
    for f in sorted(d.glob("*.sage"))
    if f.is_file()
}


def attack_path(name):
    try:
        return installed[name]
    except KeyError:
        pass
    try:
        return resources.path(builtin_attacks, builtin[name])
    except KeyError:
        pass
    raise ValueError(f"There is no attack named '{name}'")


