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

    def __init__(self):
        self.id = None

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
        mls = []
        # id 初始为 None, 需要改变
        for i, v in enumerate(ms):
            v.id = i + 1
            mls.append(v)
        return mls

    @classmethod
    def add(cls, model):
        """
        增加一个 model
        """
        models = cls.all()
        # 新加的 id 需要重设 id
        model.id = len(models) + 1
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

    @classmethod
    def find_by(cls, **kwargs):
        """
        不定参数为 username='gua'
        返回一个 username 为 'gua' 的 User 实例
        """
        for k, v in kwargs.items():
            ms = cls.all()
            for m in ms:
                # 或者使用 m.__dict__[k] == v:
                if getattr(m, k, None) == v:
                    return m
            return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        不定参数为 username='gua'
        以 list 的形式返回所有 username 属性为 'gua' 的 Model 实例
        """
        models = []
        for k, v in kwargs.items():
            ms = cls.all()
            for m in ms:
                if getattr(m, k, None) == v:
                    models.append(m)
        return models

    def __repr__(self):
        """
        当调用 str(o) 的时候
        实际上调用了 o.__str__()
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
