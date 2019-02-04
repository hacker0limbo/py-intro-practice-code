import unittest
import sqlite3
from pathlib import Path
from models import load


def select(cursor):
    sql = '''
    SELECT
        *
    FROM
        User
    WHERE
        id=1
    '''
    cursor.execute(sql)
    return cursor.fetchall()


def find_by(cursor, **kwargs):
    for k, v in kwargs.items():
        sql = f'''
        SELECT
            *
        FROM
            User
        WHERE
            {k}=?
        LIMIT
            1
        '''
        cursor.execute(sql, (v,))
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        return result


def find_all(cursor, **kwargs):
    for k, v in kwargs.items():
        sql = f'''
        SELECT
            *
        FROM
            User
        WHERE
            {k}=?
        '''
        cursor.execute(sql, (v,))
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        return result


class TestDataBase(unittest.TestCase):

    def setUp(self):
        root = Path(__file__).parent.parent
        db_path = str(root / 'db/data.sqlite')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        print("打开了数据库")

    def tearDown(self):
        # 写入数据库
        # self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print('关闭了数据库')

    def test_select(self):
        self.assertListEqual(select(self.cursor), [(1, 'gua', '41c1357e5816bf7941a490d8fb169220', '吃瓜')])

    def test_find_by(self):
        self.assertListEqual(find_by(self.cursor, username='gua'),
                             [(1, 'gua', '41c1357e5816bf7941a490d8fb169220', '吃瓜')])
        self.assertListEqual(find_by(self.cursor, password='41c1357e5816bf7941a490d8fb169220'),
                             [(1, 'gua', '41c1357e5816bf7941a490d8fb169220', '吃瓜')])
        self.assertIsNone(find_by(self.cursor, username='fuck'))

    def test_find_all(self):
        self.assertListEqual(find_all(self.cursor, username='gua'),
                             [(1, 'gua', '41c1357e5816bf7941a490d8fb169220', '吃瓜')])
        self.assertListEqual(find_all(self.cursor, password='41c1357e5816bf7941a490d8fb169220'),
                             [(1, 'gua', '41c1357e5816bf7941a490d8fb169220', '吃瓜'),
                              (2, 'limboer', '41c1357e5816bf7941a490d8fb169220', '吃饭')])
        self.assertIsNone(find_all(self.cursor, username='fuck'))

    def test_load(self):
        self.assertListEqual(load('User'), [{'id': 1,
                                         'note': '吃瓜',
                                         'password': '41c1357e5816bf7941a490d8fb169220',
                                         'username': 'gua'},
                                        {'id': 2,
                                         'note': '吃饭',
                                         'password': '41c1357e5816bf7941a490d8fb169220',
                                         'username': 'limboer'}])


if __name__ == '__main__':
    unittest.main()
