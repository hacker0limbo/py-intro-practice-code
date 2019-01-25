from main.array import (
    chunk,
    compact,
    concat,
    difference,
    difference_by,
    difference_with,
    drop,
    drop_right,
    drop_right_while,
    drop_while,
    fill,
    find_index,
    find_last_index,
    flatten,
    flatten_deep,
    flatten_depth,
    from_pairs,
    head,
    index_of,
    initial,
    intersection,
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
        self.assertListEqual(drop([1, 2, 3, 4, 5], ), [2, 3, 4, 5])
        self.assertListEqual(drop([1, 2, 3, 4, 5], 1), [2, 3, 4, 5])
        self.assertListEqual(drop([1, 2, 3, 4, 5], 2), [3, 4, 5])
        self.assertListEqual(drop([1, 2, 3, 4, 5], 5), [])
        self.assertListEqual(drop([1, 2, 3, 4, 5], 6), [])

    def test_drop_right(self):
        self.assertListEqual(drop_right([1, 2, 3, 4, 5], ), [1, 2, 3, 4])
        self.assertListEqual(drop_right([1, 2, 3, 4, 5], 1), [1, 2, 3, 4])
        self.assertListEqual(drop_right([1, 2, 3, 4, 5], 2), [1, 2, 3])
        self.assertListEqual(drop_right([1, 2, 3, 4, 5], 5), [])
        self.assertListEqual(drop_right([1, 2, 3, 4, 5], 6), [])

    def test_drop_right_while(self):
        self.assertListEqual(drop_right_while([1, 2, 3, 4, 5], lambda item: item > 3), [1, 2, 3])
        self.assertListEqual(drop_right_while([1, 2, 3, 4, 5], lambda v, i: v * i > 3), [1, 2])

    def test_drop_while(self):
        self.assertListEqual(drop_while([1, 2, 3, 4, 5], lambda item: item < 3), [3, 4, 5])

    def test_fill(self):
        a1 = [1, 2, 3, 4, 5]
        fill(a1, 0)
        self.assertListEqual(a1, [0, 0, 0, 0, 0])

        a2 = [1, 2, 3, 4, 5]
        fill(a2, 0, 2)
        self.assertListEqual(a2, [1, 2, 0, 0, 0])

        a3 = [1, 2, 3, 4, 5]
        fill(a3, 0, 2, 3)
        self.assertListEqual(a3, [1, 2, 0, 4, 5])

        a4 = [1, 2, 3, 4, 5]
        fill(a4, 0, 0, 8)
        self.assertListEqual(a4, [0, 0, 0, 0, 0])

    def test_find_index(self):
        self.assertEqual(find_index(['apple', 'banana', 'beet'], lambda item: item.startswith('b')), 1)
        self.assertEqual(find_index([{'name': 'apple', 'type': 'fruit'},
                                     {'name': 'banana', 'type': 'fruit'},
                                     {'name': 'beet', 'type': 'vegetable'}],
                                    {'name': 'banana'}),
                         1)
        self.assertEqual(find_index(['apple', 'banana', 'beet'], lambda: False), -1)

    def test_find_last_index(self):
        self.assertEqual(find_last_index(['apple', 'banana', 'beet'], lambda item: item.startswith('b')), 2)
        self.assertEqual(find_last_index([{'name': 'apple', 'type': 'fruit'},
                                          {'name': 'banana', 'type': 'fruit'},
                                          {'name': 'beet', 'type': 'vegetable'}],
                                         {'type': 'fruit'}),
                         1),
        self.assertEqual(find_last_index(['apple', 'banana', 'beet'], lambda: False), -1)

    def test_flatten(self):
        self.assertEqual(flatten([1, ['2222'], [3, [[4]]]]), [1, '2222', 3, [[4]]])

    def test_flatten_deep(self):
        self.assertEqual(flatten_deep([1, [2, [3, [4]], 5]]), [1, 2, 3, 4, 5])

    def test_flatten_depth(self):
        self.assertEqual(flatten_depth([1, [2, [3, [4]], 5]]), [1, 2, [3, [4]], 5])
        self.assertEqual(flatten_depth([1, [2, [3, [4]], 5]], 2), [1, 2, 3, [4], 5])

    def test_from_pairs(self):
        self.assertDictEqual(from_pairs([['a', 1], ['b', 2]]), {'a': 1, 'b': 2})
        self.assertDictEqual(from_pairs([['a', 1], ['b', 2], ['c', 3]]), {'a': 1, 'b': 2, 'c': 3})

    def test_head(self):
        self.assertEqual(head([1, 2, 3]), 1),
        self.assertEqual(head([]), None)

    def test_index_of(self):
        self.assertEqual(index_of([1, 2, 3, 1, 2, 3], 2, 0), 1),
        self.assertEqual(index_of([1, 2, 3, 1, 2, 3], 2, 3), 4),
        self.assertEqual(index_of([1, 1, 2, 2, 3, 3], 4, 0), -1),
        self.assertEqual(index_of([1, 1, 2, 2, 3, 3], 2, 10), -1),
        self.assertEqual(index_of([1, 1, 2, 2, 3, 3], 0, 0), -1),

    def test_initial(self):
        self.assertListEqual(initial([1, 2, 3]), [1, 2])
        self.assertListEqual(initial([1]), [])

    def test_intersection(self):
        self.assertListEqual(intersection([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2]),
        self.assertListEqual(intersection([1, 1, 2, 2], [1, 1, 2, 2]), [1, 2]),
        self.assertListEqual(intersection([1, 2, 3], [4]), []),
        self.assertListEqual(intersection([1, 2, 3],), [1, 2, 3]),
        self.assertListEqual(intersection([], [101, 2, 1, 10], [2, 1]), []),
        self.assertListEqual(intersection([],), [])


if __name__ == '__main__':
    unittest.main()
