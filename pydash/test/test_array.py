from main.array import chunk, compact, concat
import unittest


class TestArray(unittest.TestCase):
    """Test function from array.py"""

    def test_chunk(self):
        self.assertListEqual(chunk([1, 2, 3, 4, 5], ), [[1], [2], [3], [4], [5]])
        self.assertListEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        self.assertListEqual(chunk([1, 2, 3, 4, 5], 3), [[1, 2, 3], [4, 5]])
        self.assertListEqual(chunk([1, 2, 3, 4, 5], 4), [[1, 2, 3, 4], [5]])
        self.assertListEqual(chunk([1, 2, 3, 4, 5], 5), [[1, 2, 3, 4, 5]])
        self.assertListEqual(chunk([1, 2, 3, 4, 5], 6), [[1, 2, 3, 4, 5]])

    def test_compact(self):
        self.assertListEqual(compact([0, 1, 2, 3]), [1, 2, 3]),
        self.assertListEqual(compact([True, False, None, True, 1, 'foo']), [True, True, 1, 'foo'])

    def test_concat(self):
        self.assertListEqual(concat([],), []),
        self.assertListEqual(concat([1, 2, 3],), [1, 2, 3]),
        self.assertListEqual(concat([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
        self.assertListEqual(concat([1, 2, 3], [4, 5, 6], [7]), [1, 2, 3, 4, 5, 6, 7]),
        self.assertListEqual(concat([1], 2, [3], 4), [1, 2, 3, 4]),
        self.assertListEqual(concat([1], 2, [3], [[4]]), [1, 2, 3, [4]]),


if __name__ == '__main__':
    unittest.main()
