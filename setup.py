from pathlib import Path
from setuptools import setup
import shlex

def clean_sage_files(directory: Path):
    """Removes compiled Sage files from the specified directory."""
    for file_path in directory.glob("**/*.sage.py"):
        if file_path.is_file():
            file_path.unlink(missing_ok=True)
            print(f"Removed {shlex.quote(str(file_path))}")

print("Cleaning up compiled Sage files...")
clean_sage_files(Path("rsarmageddon"))

setup()
