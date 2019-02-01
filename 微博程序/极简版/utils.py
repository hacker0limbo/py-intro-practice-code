import random
import hashlib


def log(*args, **kwargs):
    print(*args, **kwargs)


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def hashed_password(pwd):
    """
    可以将一个明文密码通过 摘要算法加密为一个密文
    """
    p = pwd.encode('ascii')
    s = hashlib.sha1(p)
    return s.hexdigest()


def salted_password(password, salt='$@*$(@@(*&'):
    """
    格式为: md5(md5(pwd) + salt)
    """
    def md5hex(ascii_str):
        return hashlib.md5(ascii_str.encode('ascii')).hexdigest()
    hash1 = md5hex(password)
    hash2 = md5hex(hash1 + salt)
    return hash2
