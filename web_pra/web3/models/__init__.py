import json

def save(data, path):
    """
    将一个 list 或者 dict 写入文件中
    dumps 将一个对象转为 json 格式的字符串
    default=lambda o: o.__dict__ 可以将传进来的对象属性转为 字典
    """
    s = json.dumps(data, indent=2, ensure_ascii=False, default=lambda o: o.__dict__)
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

    @classmethod
    def db_path(cls):
        class_name = cls.__name__
        path = f'db/{class_name}.txt'
        return path

    @classmethod
    def all(cls):
        """
        这里使用 classmethod 的原因是对于一个实例是无法获得所以数据, 除非新建一个类保存所有实例
        从数据库里面读取所有数据, 转为对象以后返回
        """
        path = cls.db_path()
        models = load(path)
        # models 是字典格式, 需要转为 对象
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def add(cls, model):
        models = cls.all()
        models.append(model)
        cls.save(models)

    @classmethod
    def save(cls, models):
        """
        将一个新的实例保存到数据库中
        """
        # 将一个对象的属性转为字典才能写入数据库, save 函数已经做了, 不用再转换
        l = [m for m in models]
        path = cls.db_path()
        # 写入数据库
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
