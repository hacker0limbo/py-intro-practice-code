import unittest
from web1.h1 import (
    protocol_of_url,
    host_of_url,
    port_of_url,
    path_of_url,
    parsed_url,
)


class TestH1(unittest.TestCase):

    def test_protocol_of_url(self):
        self.assertEqual(protocol_of_url('g.cn'), 'http')
        self.assertEqual(protocol_of_url('g.cn/'), 'http')
        self.assertEqual(protocol_of_url('g.cn:3000'), 'http')
        self.assertEqual(protocol_of_url('g.cn:3000/search'), 'http')
        self.assertEqual(protocol_of_url('http://g.cn'), 'http')
        self.assertEqual(protocol_of_url('https://g.cn'), 'https')
        self.assertEqual(protocol_of_url('http://g.cn/'), 'http')

    def test_host_of_url(self):
        self.assertEqual(host_of_url('g.cn'), 'g.cn')
        self.assertEqual(host_of_url('g.cn/'), 'g.cn')
        self.assertEqual(host_of_url('g.cn:3000'), 'g.cn')
        self.assertEqual(host_of_url('g.cn:3000/search'), 'g.cn')
        self.assertEqual(host_of_url('http://g.cn'), 'g.cn')
        self.assertEqual(host_of_url('https://g.cn'), 'g.cn')
        self.assertEqual(host_of_url('http://g.cn/'), 'g.cn')
        self.assertEqual(host_of_url('http://g.cn:3000/search'), 'g.cn')

    def test_port_of_url(self):
        self.assertEqual(port_of_url('g.cn'), 80)
        self.assertEqual(port_of_url('g.cn/'), 80)
        self.assertEqual(port_of_url('g.cn:3000'), 3000)
        self.assertEqual(port_of_url('g.cn:3000/search'), 3000)
        self.assertEqual(port_of_url('http://g.cn'), 80)
        self.assertEqual(port_of_url('https://g.cn'), 443)
        self.assertEqual(port_of_url('http://g.cn/'), 80)
        self.assertEqual(port_of_url('http://g.cn:3000/search'), 3000)
        self.assertEqual(port_of_url('https://g.cn:3000/search'), 3000)

    def test_path_of_url(self):
        self.assertEqual(path_of_url('g.cn'), '/')
        self.assertEqual(path_of_url('g.cn/'), '/')
        self.assertEqual(path_of_url('g.cn:3000'), '/')
        self.assertEqual(path_of_url('g.cn:3000/search'), '/search')
        self.assertEqual(path_of_url('http://g.cn'), '/')
        self.assertEqual(path_of_url('https://g.cn'), '/')
        self.assertEqual(path_of_url('http://g.cn/'), '/')
        self.assertEqual(path_of_url('http://g.cn:3000/search'), '/search')

    def test_parsed_url(self):
        http = 'http'
        https = 'https'
        host = 'g.cn'
        path = '/'
        self.assertEqual(parsed_url('http://g.cn'), (http, host, 80, path))
        self.assertEqual(parsed_url('http://g.cn/'), (http, host, 80, path))
        self.assertEqual(parsed_url('http://g.cn:90'), (http, host, 90, path))
        self.assertEqual(parsed_url('http://g.cn:90/'), (http, host, 90, path))
        self.assertEqual(parsed_url('https://g.cn'), (https, host, 443, path))
        self.assertEqual(parsed_url('https://g.cn:233/'), (https, host, 233, path))

    def setUp(self):
        print('当前测试开始')

    def tearDown(self):
        print('当前测试结束')

    @classmethod
    def setUpClass(cls):
        print('所有测试开始')

    @classmethod
    def tearDownClass(cls):
        print('所有测试结束')


if __name__ == '__main__':
    unittest.main(verbosity=2)