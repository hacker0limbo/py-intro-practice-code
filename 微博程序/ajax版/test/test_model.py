from models import Model, load, dbopen
import unittest

"""
测试 Model 类
1, 测试开始前创建一个虚拟表 Student, 拥有 id 和 name 字段
2, 在测试结束后删除该表
3, 创建虚拟类 Student, 拥有 id 和 name 属性
"""


class Student(Model):
    """Student 为测试对象, 拥有 id 和 name 属性"""
    def __init__(self, form):
        self.id = form.get('id', -1)
        self.name = form.get('name', '')

    @classmethod
    def select_last(cls):
        sql = f"""
        SELECT
            *
        FROM
            {cls.__name__}
        ORDER BY
            id
        DESC LIMIT 1 
        """
        with dbopen() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()


class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """创建虚拟表 Student 并插入数据"""
        cls.create_db()
        cls.insert_data()

    @classmethod
    def tearDownClass(cls):
        """drop Student 表"""
        cls.drop_db()

    @classmethod
    def create_db(cls):
        sql_create = '''
        CREATE TABLE IF NOT EXISTS `Student` (
            `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `name`  TEXT
        );
        '''
        with dbopen() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_create)
        print('创建了 Student 数据库')

    @classmethod
    def insert_data(cls):
        sql_insert = '''
        INSERT INTO
            Student(name)
        VALUES
            (?);
        '''
        data = [('gua',), ('gw',)]
        with dbopen() as conn:
            cursor = conn.cursor()
            cursor.executemany(sql_insert, data)
        print('Student 表增加了数据')

    @classmethod
    def drop_db(cls):
        sql_drop = """
        DROP TABLE IF EXISTS Student;
        """
        with dbopen() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_drop)
        print('删除了表 Student')

    def test_load(self):
        r = [
            {
                'id': 1,
                'name': 'gua',
            },
            {
                'id': 2,
                'name': 'gw'
            },
        ]
        self.assertListEqual(load('Student'), r)

    def test_all(self):
        r = [
            {
                'id': 1,
                'name': 'gua',
            },
            {
                'id': 2,
                'name': 'gw'
            },
        ]
        ss = Student.all()
        l = [s.__dict__ for s in ss]
        self.assertListEqual(l, r)

    def test_find_by(self):
        s1 = Student.find_by(id=1)
        s2 = Student.find_by(name='gw')
        self.assertEqual(s1.name, 'gua')
        self.assertEqual(s2.id, 2)

    def test_find_all(self):
        r = [
            {
                'id': 1,
                'name': 'gua',
            },
        ]
        ss = Student.find_all(name='gua')
        l = [s.__dict__ for s in ss]
        self.assertListEqual(l, r)

    def test_add_and_delete(self):
        form = {
            'id': 3,
            'name': 'bobo'
        }
        s = Student(form)
        Student.add(s)
        Student.delete(3)
        self.assertListEqual(Student.select_last(), [(2, 'gw')])

    def test_update(self):
        Student.update(2, name='bobo')
        self.assertListEqual(Student.select_last(), [(2, 'bobo')])
        Student.update(2, name='gw')
        self.assertListEqual(Student.select_last(), [(2, 'gw')])



if __name__ == '__main__':
    unittest.main()

