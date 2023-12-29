from pathlib import Path
from setuptools import setup
import shlex

def sh_escape(file_path):
    """Shell-escapes the file path."""
    return shlex.quote(str(file_path))

def clean_sage_files(directory: Path):
    """Removes compiled Sage files from the specified directory."""
    for file_path in directory.glob("**/*.sage.py"):
        if file_path.is_file():
            try:
                file_path.unlink(missing_ok=True)
                print(f"Removed {sh_escape(file_path)}")
            except OSError as e:
                print(f"Error removing {sh_escape(file_path)}: {e}")

print("Cleaning up compiled Sage files...")
clean_sage_files(Path("rsarmageddon"))

setup()
