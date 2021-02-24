import os
import re
from pathlib import Path
from importlib import resources
from importlib.resources import contents, is_resource

import builtin_attacks


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


