"""
checksums
"""
import sys
import hashlib

def sha256_file_checksum(file_path: str) -> str:
    hash_sha256 = hashlib.sha256()
    try:
        """
        from a tip that i saw here: https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
        """
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
    except OSError as e:
        print("hash_sum.py:sha256_file_checksum ->", e)
        sys.exit(1)
    return hash_sha256.hexdigest()