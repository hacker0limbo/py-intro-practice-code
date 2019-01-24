from main.array import (
    chunk,
    compact,
    concat,
    difference,
    difference_by,
    difference_with,
    drop,
)
import unittest
import math


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
        self.assertListEqual(concat([], ), []),
        self.assertListEqual(concat([1, 2, 3], ), [1, 2, 3]),
        self.assertListEqual(concat([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
        self.assertListEqual(concat([1, 2, 3], [4, 5, 6], [7]), [1, 2, 3, 4, 5, 6, 7]),
        self.assertListEqual(concat([1], 2, [3], 4), [1, 2, 3, 4]),
        self.assertListEqual(concat([1], 2, [3], [[4]]), [1, 2, 3, [4]]),

    def test_difference(self):
        self.assertListEqual(difference([3, 2, 1], [4, 2]), [3, 1])
        self.assertListEqual(difference([1, 2, 3, 4], ), [1, 2, 3, 4])
        self.assertListEqual(difference([1, 2, 3, 4], []), [1, 2, 3, 4])
        self.assertListEqual(difference([1, 2, 3, 4], [2, 4], [3, 5, 6]), [1])
        self.assertListEqual(difference([1, 1, 1, 1], [2, 4], [3, 5, 6]), [1, 1, 1, 1])

    @unittest.skip('difference_by 未完成')
    def test_difference_by(self):
        self.assertListEqual(difference_by([3.1, 2.2, 1.3], [4.4, 2.5], math.floor), [3.1, 1.3])
        self.assertListEqual(difference_by([{'a': 1}, {'a': 2, 'b': 2}], [{'a': 1}], 'a'), [{'a': 2, 'b': 2}])

    @unittest.skip('difference_with 未完成')
    def test_difference_with(self):
        self.assertListEqual(difference_with([1, 2, 3, 4], ), [1, 2, 3, 4])
        self.assertListEqual(difference_with([1, 2, 3, 4], []), [1, 2, 3, 4])
        self.assertListEqual(difference_with([{'a': 1}, {'a': 2, 'b': 2}],
                                             [{'a': 1}], lambda item, other: item['a'] == other['a']),
                             [{'a': 2, 'b': 2}])

    def test_drop(self):
        self.assertListEqual(drop([1, 2, 3, 4, 5],), [2, 3, 4, 5]),
        self.assertListEqual(drop([1, 2, 3, 4, 5], 1), [2, 3, 4, 5]),
        self.assertListEqual(drop([1, 2, 3, 4, 5], 2), [3, 4, 5]),
        self.assertListEqual(drop([1, 2, 3, 4, 5], 5), []),
        self.assertListEqual(drop([1, 2, 3, 4, 5], 6), []),


if __name__ == '__main__':
    unittest.main()
