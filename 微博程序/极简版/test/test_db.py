import unittest
import sqlite3
from pathlib import Path


""""
三种方法减少连接数据库的代码
1, 使用 with 自动 commit/rollback
2, 使用装饰器在执行 query 前后自动打开关闭数据库
3, 自己写一个上下文管理器自动管理资源
"""

root = Path(__file__).parent.parent
db_path = str(root / 'db/data.sqlite')


def dbconn(query):
    def wrapper(cls, *args, **kwargs):
        conn = sqlite3.connect(db_path)
        result = query(cls, conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper


def db_conn(query):
    def wrapper(cls, *args, **kwargs):
        conn = sqlite3.connect(db_path)
        with conn:
            # with 不自动关闭, 需要手动关闭, with 只帮助处理 commit 或 rollback
            result = query(cls, conn, *args, **kwargs)
        conn.close()
        return result
    return wrapper


class dbopen:
    """
    上下文管理器, 自动释放资源
    """
    def __init__(self, path=db_path):
        self.path = path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()



class Student:

    @classmethod
    @dbconn
    def select_all(cls, conn):
        cursor = conn.cursor()
        sql = """
        SELECT
            *
        FROM
            Student
        """
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    @db_conn
    def select_first(cls, conn):
        cursor = conn.cursor()
        sql = """
        SELECT
            *
        FROM
            Student
        WHERE
            id=1
        """
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def select_second(cls):
        sql = """
        SELECT
            *
        FROM
            Student
        WHERE
            id=2
        """
        with dbopen() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


class TestDataBase(unittest.TestCase):

    def test_select_all(self):
        self.assertListEqual(Student.select_all(), [(1, 'gua'), (2, 'gw')])

    def test_select_one(self):
        self.assertListEqual(Student.select_first(), [(1, 'gua')])

    def test_select_two(self):
        self.assertListEqual(Student.select_second(), [(2, 'gw')])


if __name__ == '__main__':
    unittest.main()
