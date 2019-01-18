import json

def save(data, path):
    """
    将一个 list 或者 dict 写入文件中
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        print('文件写入成功')
        f.write(s)


def load(path):
    """
    从一个文件中载入数据并转化为 dict 或者 list
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        print('文件读取成功')
        return json.loads(s)


class Model:

    def __init__(self, data):
        self.data = data

    def db_path(self):
        class_name = self.__class__.__name__
        path = f'db/{class_name}.txt'
        return path

    def all(self):
        """
        从数据库里面读取所有数据, 转为对象以后返回
        """
        path = self.db_path()
        models = load(path)
        # models 是字典格式, 需要转为 对象
        ms = [self.__class__(m) for m in models]
        return ms

    def save(self):
        models = self.all()
        models.append(self)
        # 将一个对象的属性转为字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        当调用 str(o) 的时候
        实际上调用了 o.__str__()
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
