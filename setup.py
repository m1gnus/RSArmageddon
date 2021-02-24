from pathlib import Path
from setuptools import setup

def sh_escape(f):
    f = str(f).replace("'", r"'\''")
    return f"'{f}'"

print("cleaning up compiled sage files")
for f in Path("rsarmageddon").glob("**/*.sage.py"):
    if not f.is_dir():
        f.unlink(missing_ok=True)
        print(f"removed {sh_escape(f)}")

setup()
