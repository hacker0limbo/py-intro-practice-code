import hashlib


def sha256(ascii_str):
    return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
