"""
checksums
"""
import sys
import hashlib

def md5_file_checksum(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    try:
        hash_md5.update(open(file_path, "rb").read())
    except OSError as e:
        print("hash_sum.py:md5_file_checksum ->", e)
        sys.exit(1)
    return hash_md5.hexdigest()