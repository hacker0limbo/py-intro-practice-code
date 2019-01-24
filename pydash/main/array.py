def chunk(array: list, size: int=1) -> list:
    """
    将数组（array）拆分成多个 size 长度的区块，并将这些区块组成一个新数组
    如果array 无法被分割成全部等长的区块，那么最后剩余的元素将组成一个区块

    :param array: 需要处理的数组
    :param size: 每个数组区块的长度
    :return: 一个包含拆分区块的新数组
    """
    return [array[i:i+size] for i in range(0, len(array), size)]


def compact(array: list) -> list:
    """
    创建一个新数组，包含原数组中所有的非假值元素
    例如false, null, 0, "", undefined, 和 NaN 都是被认为是“假值”

    :param array:
    :return:
    """
    return [x for x in array if x]


def concat(array: list, *args) -> list:
    """
    创建一个新数组，将array与任何数组 或 值连接在一起
    :param array:
    :param args:
    :return:
    """
    result = array[:]
    for v in args:
        if type(v) is list:
            result.extend(v)
        else:
            result.append(v)
    return result


def difference(array: list, *args) -> list:
    """
    创建一个新数组，这个数组中的值，为第一个数组（array 参数）排除了给定数组中的值
    :param array:
    :param args:
    :return:
    """
    t = []
    result = []
    for v in args:
        t.extend(v)
    for a in array:
        if a in t:
            continue
        result.append(a)
    return result


def identity(*args):
    """
    返回首个提供的参数
    :param args:
    :return:
    """
    return args[0]


def difference_by(array, *args):
    """
    接受一个迭代器 iteratee 调用 array 和 values 中的每个元素以产生比较的标准
    结果值从第一个数组中选择
    :param array:
    :param args:
    :return:
    """
    iteratee = args[-1]
    a = [iteratee(x) for x in array]
    vs = [[iteratee(v) for v in arg] for arg in args[:-1]]
    t = []
    for v in vs:
        t.extend(v)
    result = []
    for i, v in enumerate(a):
        if v in t:
            continue
        result.append(array[i])
    return result


def difference_with(array, *args):
    pass


def drop(array, n=1):
    """
    创建一个切片数组，去除 array 前面的 n 个元素
    :param array:
    :param n:
    :return:
    """
    return array[n:]


def drop_right(array, n=1):
    """
    创建一个切片数组，去除array尾部的n个元素
    :param array:
    :param n:
    :return:
    """
    return array[:-n]