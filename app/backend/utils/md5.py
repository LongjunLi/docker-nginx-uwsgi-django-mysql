import hashlib


def calculate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode("utf-8"))
    return md5_hash.hexdigest()
