import unittest
from h2 import (
    path_with_query,
    header_from_dict,
    value_from_element,
)


class TestH1(unittest.TestCase):

    def test_path_with_query(self):
        path = '/'
        query = {
            'name': 'gua',
            'height': 169,
        }
        expected = [
            '/?name=gua&height=169',
            '/?height=169&name=gua',
        ]
        self.assertIn(path_with_query(path, query), expected)

    def test_header_from_dict(self):
        headers = {
            'Content-Type': 'text/html',
            'Content-Length': 127,
        }
        header = 'Content-Type: text/html\r\nContent-Length: 127\r\n'
        self.assertEqual(header_from_dict(headers), header)

    def test_value_from_element(self):
        html = """<ol>
            <li class="name">gua</li>
        </ol>
        """
        element = '<li class="name">gua</li>'
        self.assertEqual(value_from_element(html, element), 'gua')

    @classmethod
    def setUpClass(cls):
        print('所有测试开始')

    @classmethod
    def tearDownClass(cls):
        print('所有测试结束')


if __name__ == '__main__':
    unittest.main(verbosity=2)
