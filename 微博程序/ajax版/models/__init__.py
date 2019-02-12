import sqlite3
from pathlib import Path


class dbopen:
    """
    上下文管理器, 自动释放资源
    """
    def __init__(self, path=None):
        root = Path(__file__).parent.parent
        db_path = str(root / 'db/data.sqlite')
        if path is None:
            # 默认为 data.sqlite 这个数据库
            self.path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


def dict_factory(cursor, row):
    """
    改变数据库返回数据的格式, 为一个字典
    """
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    return d


def load(table):
    """
    从数据里面读取数据, 并返回一个列表, 包含字典, 每个字典代表一组数据, 如下:
    [
      {
        'id': 1,
        'username': xxx
      },
    ]
    """
    with dbopen() as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        sql = f"""
        SELECT
            *
        FROM
            {table}
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


class Model:

    @classmethod
    def all(cls):
        """
        从数据库里面读取所有数据并生成对象
        """
        table = cls.__name__
        models = load(table)
        # models 是字典格式, 需要转为 对象
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        不定参数为 username='gua'
        返回一个 username 为 'gua' 的 Model 实例
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

    @classmethod
    def add(cls, m):
        """
        往数据库里面添加一个新的数据
        """
        m_attr = m.__dict__
        attr = {k: v for k, v in m_attr.items() if k != 'id'}
        columns = ', '.join(attr.keys())
        placeholders = ', '.join('?' * len(attr))
        sql_insert = f"""
        INSERT INTO
            {cls.__name__}({columns})
        VALUES
            ({placeholders});
        """
        with dbopen() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_insert, tuple(attr.values()))

    @classmethod
    def delete(cls, id):
        sql_delete = f'''
        DELETE FROM
            {cls.__name__}
        WHERE
            id=?
        '''
        with dbopen() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_delete, (id,))

    @classmethod
    def update(cls, id, **kwargs):
        """
        根据 id 更新表中的一个数据, **kwargs 为 字段=值 这种形式
        """
        columns = ', '.join([f'`{k}`=?'for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (id,)
        sql_update = f'''
        UPDATE
            {cls.__name__}
        SET
            {columns}
        WHERE
            id=?
        '''
        with dbopen() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_update, values)

    def __repr__(self):
        """
        当调用 str(o) 的时候
        实际上调用了 o.__str__()
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
