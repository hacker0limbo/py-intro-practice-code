import unittest
from models import open_db, close_db
from models.user import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.conn, self.cursor = open_db()
        print("打开了数据库")

    def tearDown(self):
        # 写入数据库
        close_db(self.conn, self.cursor)
        print('关闭了数据库')

    def last_row_id(self):
        sql = """
        SELECT
            id
        FROM
            User
        ORDER BY
            id
        DESC LIMIT 1
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def test_add(self):
        form = {
            'username': 'gua1',
            'password': '321',
            'note': 'lol',
        }
        u = User(form)
        User.add(self.cursor, u)
        self.assertEqual(self.last_row_id(), self.cursor.lastrowid)


if __name__ == '__main__':
    unittest.main()
