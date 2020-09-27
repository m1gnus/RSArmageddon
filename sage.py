import os
import sys
import re
import shutil
import subprocess

from subprocess import PIPE


INSTALL_SAGE_POSIX = "Sage install instructions for *NIX systems"
INSTALL_SAGE_NT = "Sage install instructions for Windows systems"
NO_JAVA = "This program cannot run on Jython and other Java based execution environments"

SUPPORTED_VMAJ = 9

sage = None


def version(sage):
    p = subprocess.run([sage, "--version"], capture_output=True, text=True)
    m = re.search(r"(\d+)\.(\d+)", p.stdout, re.ASCII)
    if not m:
        raise RuntimeError(f"SageMath version could not be identified. Version string: {p.stdout}", file=sys.stderr)
    vmaj, vmin = m.group(1, 2)
    return int(vmaj), int(vmin)


def get_sage_posix():
    sage = shutil.which("sage")
    if sage is None:
        raise RuntimeError(INSTALL_SAGE_POSIX)
    return sage


def get_sage_nt():
    raise NotImplementedError


def get_sage_java():
    raise RuntimeError(NO_JAVA)


def get_sage():
    global sage
    if sage is not None:
        return sage
    get_sage_by_platform = {
        "posix": get_sage_posix,
        "nt": get_sage_nt,
        "java": get_sage_java
    }
    sage = get_sage_by_platform[os.name]()
    vmaj, vmin = version(sage)
    if vmaj != SUPPORTED_VMAJ:
        print(f"[W] Using unsupported SageMath version {vmaj}.{vmin}", file=sys.stderr)
        print(f"[W] RSArmageddon is not supposed to work with versions other than {SUPPORTED_VMAJ}.x,", file=sys.stderr)
        print(f"[W] try installing the latest one of those before reporting a bug", file=sys.stderr)
    return sage


def run(script, *args, env=None, timeout=None):
    p = subprocess.run([get_sage(), *args], env=env, timeout=timeout, stdout=PIPE, text=True)
    return p.stdout
