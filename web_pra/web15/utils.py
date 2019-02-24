import hashlib
import time


def sha256(ascii_str):
    return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()


def current_time(time_stamp):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(time_stamp)
    dt = time.strftime(format, value)
    return dt
