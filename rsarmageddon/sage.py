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
import re
import shutil
import subprocess

from textwrap import dedent
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from itertools import count, chain
from subprocess import Popen, PIPE, TimeoutExpired
from psutil import Process, wait_procs

from .utils import output


if os.name == "nt":
    from winreg import HKEY_CURRENT_USER, OpenKey, EnumKey, QueryValueEx


INSTALL_SAGE_POSIX = dedent("""\
        We could not be able to find a functioning SageMath installation on your system.
        Please refer to these online instructions to fix this: https://github.com/m1gnus/RSArmageddon#installing-sage-manually-on-linux""")
INSTALL_SAGE_NT = dedent("""\
        We could to be able to find a functioning SageMath installation on your system.
        Please refer to these online instructions to fix this: https://github.com/m1gnus/RSArmageddon#installing-sage-manually-on-windows""")
NO_JAVA = "This program will not run on Jython and other Java based execution environments"

SUPPORTED_VMAJ = 9


def best_version(versions):
    supported = [(vmaj, vmin) for vmaj, vmin in versions if vmaj == SUPPORTED_VMAJ]
    if supported:
        return max(supported)
    return max(versions)


def cyg_path(path, cyg_runtime):
    path = Path(path)
    if cyg_runtime is None:
        return PurePosixPath(path)
    cyg_runtime = Path(cyg_runtime)
    p = subprocess.run(
            [str(cyg_runtime/"bin"/"cygpath.exe"), str(path)],
            stdout=PIPE, text=True) # TODO: is Unicode handled properly?
    return PurePosixPath(p.stdout[:-1])


def cyg_bash(cyg_runtime):
    if cyg_runtime is None:
        return []
    cyg_runtime = Path(cyg_runtime)
    return [str(cyg_runtime/"bin"/"bash.exe"), "--norc", "--login"]


version_re = re.compile(r"(\d+)\.(\d+)", re.ASCII)

def version(sage, cyg_runtime=None):
    sage = PurePosixPath(sage)
    p = subprocess.run(
            [*cyg_bash(cyg_runtime), str(sage), "--version"],
            stdout=PIPE, text=True)
    m = version_re.search(p.stdout)
    if not m:
        raise RuntimeError(f"SageMath version could not be identified (not a sage executable?). Version string: {p.stdout}")
    vmaj, vmin = m.group(1, 2)
    return int(vmaj), int(vmin)


def get_sage_nt_locations_registry():
    assert os.name == "nt"
    sage_key_re = re.compile(r"SageMath-(\d+)\.(\d+)", re.IGNORECASE)
    with OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as root_key:
        try:
            for i in count():
                subkey_name = EnumKey(root_key, i)
                m = sage_key_re.search(subkey_name)
                if m:
                    vmaj, vmin = m.group(1, 2)
                    with OpenKey(root_key, subkey_name) as subkey:
                        location, _ = QueryValueEx(subkey, "InstallLocation")
                    yield Path(location).resolve(), vmaj, vmin
        except OSError:
            pass


def get_sage_nt_locations_appdata():
    assert os.name == "nt"
    try:
        appdata = Path(os.environ.get("LOCALAPPDATA", os.environ["APPDATA"]))
    except KeyError as e:
        raise RuntimeError("Cannot find the AppData folder! Is this a sane Windows machine?") from e
    for subdir in appdata.glob("sagemath*"):
        m = version_re.search(subdir.name)
        if m:
            vmaj, vmin = m.group(1, 2)
            yield subdir.resolve(), vmaj, vmin


def get_sage_nt():
    assert os.name == "nt"
    sages_by_ver = {}
    for location, vmaj, vmin in chain(
            get_sage_nt_locations_registry(), get_sage_nt_locations_appdata()):
        cyg_runtime = location/"runtime"
        sage = PurePosixPath(f"/opt/sagemath-{vmaj}.{vmin}/local/bin/sage")
        try:
            ver = version(sage, cyg_runtime)
        except (RuntimeError, OSError):
            continue
        sages_by_ver.setdefault(ver, set()).add((sage, cyg_runtime))

    if not sages_by_ver:
        raise RuntimeError(INSTALL_SAGE_NT)

    best_ver = best_version(sages_by_ver.keys())
    return (best_ver, *sages_by_ver[best_ver].pop())


def get_sage_posix():
    sage = shutil.which("sage")
    if sage is None:
        raise RuntimeError(INSTALL_SAGE_POSIX)
    return version(sage), sage, None


def get_sage_java():
    raise RuntimeError(NO_JAVA)


sage = None
cyg_runtime = None

def get_sage():
    global sage, cyg_runtime
    if sage is not None:
        return sage, cyg_runtime
    get_sage_by_platform = {
        "posix": get_sage_posix,
        "nt": get_sage_nt,
        "java": get_sage_java
    }
    version, sage, cyg_runtime = get_sage_by_platform[os.name]()
    vmaj, vmin = version
    if vmaj != SUPPORTED_VMAJ:
        output.warning(f"Using unsupported SageMath version {vmaj}.{vmin}")
        output.warning(f"RSArmageddon is not supposed to work with versions other than {SUPPORTED_VMAJ}.x,")
        output.warning(f"try installing the latest one of those before reporting a bug")
    return sage, cyg_runtime


def run(script_path, *args, env=None, timeout=None):
    script_path = Path(script_path).resolve()
    sage, cyg_runtime = get_sage()
    with TemporaryDirectory() as writeable_dir:
        new_path = Path(writeable_dir)/script_path.name
        shutil.copy(script_path, new_path)
        p = Popen(
                [*cyg_bash(cyg_runtime), str(sage), str(cyg_path(new_path, cyg_runtime)), *args],
                stdout=PIPE, env=env, text=True)
        try:
            output, _ = p.communicate(timeout=timeout)
        except TimeoutExpired as e:
            pp = Process(p.pid)
            subprocesses = [pp, *pp.children(recursive=True)]
            for subp in subprocesses:
                subp.terminate()
            wait_procs(subprocesses)
            raise e
    return p, output
