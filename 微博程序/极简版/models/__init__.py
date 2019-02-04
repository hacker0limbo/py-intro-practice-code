import sqlite3
from pathlib import Path


def open_db():
    root = Path(__file__).parent.parent
    db_path = str(root / 'db/data.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def close_db(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
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
    conn, cursor = open_db()
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
    close_db(conn, cursor)
    return result


class Model:

    @classmethod
    def db_path(cls):
        class_name = cls.__name__
        path = f'db/{class_name}.txt'
        return path

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
    def add(cls, cursor, m):
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
        cursor.execute(sql_insert, tuple(attr.values()))

    @classmethod
    def delete(cls, cursor, id):
        sql_delete = f'''
        DELETE FROM
            {cls.__name__}
        WHERE
            id=?
        '''
        cursor.execute(sql_delete, (id,))

    @classmethod
    def update(cls, cursor, id, content):
        sql_update = f'''
        UPDATE
            {cls.__name__}
        SET
            content=?
        WHERE
            id=?
        '''
        cursor.execute(sql_update, (content, id))

    def __repr__(self):
        """
        当调用 str(o) 的时候
        实际上调用了 o.__str__()
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
