def chunk(array: list, size: int=1) -> list:
    """
    将数组（array）拆分成多个 size 长度的区块，并将这些区块组成一个新数组
    如果array 无法被分割成全部等长的区块，那么最后剩余的元素将组成一个区块

    :param array: 需要处理的数组
    :param size: 每个数组区块的长度
    :return: 一个包含拆分区块的新数组
    """
    result = []
    l = len(array)
    if size >= l:
        result.append(array[:])
    else:
        c = l // size
        v = l - l % size
        for i in range(c):
            result.append(array[i*size:i*size+size])
        if len(array[v:]) != 0:
            result.append(array[v:])
    return result


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


