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


def drop_right_while(array, predicate=None):
    """
    创建一个切片数组，去除array中从 predicate 返回假值开始到尾部的部分。
    predicate 会传入3个参数： (value, index, array)
    :param array:
    :param predicate:
    :return:
    """
    for i, v in enumerate(array):
        # 判断传入的参数的数量
        if predicate.__code__.co_argcount == 1:
            if predicate(v):
                return array[:i]
        elif predicate.__code__.co_argcount == 2:
            if predicate(v, i):
                return array[:i]
        else:
            if predicate(v, i, array):
                return array[:i]


def drop_while(array, predicate):
    """
    创建一个切片数组，去除array中从起点开始到 predicate 返回假值结束部分
    predicate 会传入3个参数： (value, index, array)
    :param array:
    :param predicate:
    :return:
    """
    for i, v in enumerate(array):
        # 判断传入的参数的数量
        if predicate.__code__.co_argcount == 1:
            if not predicate(v):
                return array[i:]
        elif predicate.__code__.co_argcount == 2:
            if not predicate(v, i):
                return array[i:]
        else:
            if not predicate(v, i, array):
                return array[i:]


def fill(array, value, start=0, end=-1):
    """
    使用 value 值来填充（替换） array，从start位置开始, 到end位置结束（但不包含end位置）
    这个方法会改变 array
    :param array:
    :param value:
    :param start:
    :param end:
    :return:
    """
    if end == -1 or end > len(array):
        end = len(array)
    for i in range(start, end):
        array[i] = value


def find_index(array, predicate, from_index=0):
    """
    该方法返回第一个通过 predicate 判断为真值的元素的索引值（index），而不是元素本身
    返回 index, 默认为 -1
    predicate 参数依次为 value, index, array

    predicate 如果是 dict
    :param array:
    :param predicate: (Array|Function|Object|string)
    :param from_index:
    :return:
    """
    for i, v in enumerate(array[from_index:]):
        if isinstance(predicate, (list, dict, str)):
            if isinstance(predicate, (list, str)):
                if array.count(predicate) > 0:
                    return array.index(predicate)
            else:
                # 是字典, predicate 可能是 sub dict, 匹配
                # 匹配 sublist 如下
                if predicate.items() <= v.items():
                    return i
        else:
            # 说明是函数, 判断参数个数
                # 判断传入的参数的数量
            if predicate.__code__.co_argcount == 0:
                if predicate():
                    return 0
                return -1
            elif predicate.__code__.co_argcount == 1:
                if predicate(v):
                    return i
            elif predicate.__code__.co_argcount == 2:
                if predicate(v, i):
                    return i
            else:
                if predicate(v, i, array):
                    return i
    return -1


def find_last_index(array, predicate, from_index=0):
    """
    这个方式类似 _.findIndex， 区别是它是从右到左的迭代集合array中的元素
    :param array:
    :param predicate:
    :param from_index:
    :return:
    """
    for i, v in reversed(list(enumerate(array[from_index:]))):
        if isinstance(predicate, (list, dict, str)):
            if isinstance(predicate, (list, str)):
                if array.count(predicate) > 0:
                    return array.index(predicate)
            else:
                # 是字典, predicate 可能是 sub dict, 匹配
                # 匹配 sublist 如下
                if predicate.items() <= v.items():
                    return i
        else:
            # 说明是函数, 判断参数个数
                # 判断传入的参数的数量
            if predicate.__code__.co_argcount == 0:
                if predicate():
                    return -1
            elif predicate.__code__.co_argcount == 1:
                if predicate(v):
                    return i
            elif predicate.__code__.co_argcount == 2:
                if predicate(v, i):
                    return i
            else:
                if predicate(v, i, array):
                    return i
    return -1


def flatten(array):
    """
    减少一级array嵌套深度
    :param array:
    :return:
    """
    result = []
    for a in array:
        if type(a) is not list:
            result.append(a)
            continue
        for v in a:
            result.append(v)
    return result


def flatten_deep(array):
    """
    将array递归为一维数组
    :param array:
    :return:
    """
    result = []
    for v in array:
        if isinstance(v, list):
            result.extend(flatten_deep(v))
        else:
            result.append(v)
    return result


def flatten_depth(array, depth=1):
    """
    根据 depth 递归减少 array 的嵌套层级
    :param array:
    :return:
    """
    result = []
    for v in array:
        if isinstance(v, list) and depth >= 1:
            # 控制递归深度
            result.extend(flatten_depth(v, depth-1))
        else:
            result.append(v)
    return result


def from_pairs(paris):
    """
    pairs 是一个由 v: k 组成的数组, 这个方法返回一个由键值对pairs构成的字典
    :param paris:
    :return:
    """
    d = {}
    for p in paris:
        d[p[0]] = p[1]
    return d


def head(array):
    """
    获取数组 array 的第一个元素
    :param array:
    :return:
    """
    if len(array) == 0:
        return None
    return array[0]


def index_of(array, value, from_index=0):
    """
    返回首次 value 在数组array中被找到的 索引值
    :param array:
    :param value:
    :param from_index:
    :return:
    """
    try:
        return array.index(value, from_index)
    except ValueError:
        return -1


def initial(array):
    """
    获取数组array中除了最后一个元素之外的所有元素
    :param array:
    :return:
    """
    return array[:-1]


def intersection(*args):
    """
    创建唯一值的数组，这个数组包含所有给定数组都包含的元素
    :param args:
    :return:
    """
    return list(set(args[0]).intersection(*args))
