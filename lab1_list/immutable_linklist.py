class SingleNode(object):
    def __init__(self, item, next=None):
        self.next = next
        self.item = item

    def __str__(self):
        """for str() implementation"""
        if type(self.next) is SingleNode:
            return "{} : {}".format(self.item, self.next)
        return str(self.item)

    def __eq__(self, other):
        """for write assertion, we should be abel for check list equality (list are equal, if all elements are equal)."""

        if other is None:
            return False
        if self.item != other.item:
            return False
        return self.next == other.next


def size(n):
    if n is None:
        return 0
    else:
        return 1 + size(n.next)


def cons(head, tail):
    """add new element to head of the list"""
    return SingleNode(head, tail)


def remove(n, element):
    assert n is not None, "element should be in list"
    if n.item == element:
        return n.next
    else:
        return cons(n.item, remove(n.next, element))


def head(n):
    assert type(n) is SingleNode
    return n.item


def tail(n):
    assert type(n) is SingleNode
    return n.next


def reverse(n, acc=None):
    if n is None:
        return acc
    return reverse(tail(n), SingleNode(head(n), acc))


def mempty():
   return None


def mconcat(a, b):
   if a is None:
      return b
   tmp = reverse(a)
   res = b
   while tmp is not None:
      res = cons(tmp.item, res)
      tmp = tmp.next
   return res

def to_list(n):
   res = []
   cur = n
   while cur is not None:
       res.append(cur.item)
       cur = cur.next
   return res


def from_list(lst):
   res = None
   for e in reversed(lst):
       res = cons(e, res)
   return res


def iterator(lst):
   cur = lst
   def foo():
      nonlocal cur
      if cur is None: raise StopIteration
      tmp = cur.item
      cur = cur.next
      return tmp
   return foo




import unittest
from hypothesis import given
import hypothesis.strategies as st
# from immutable import *


class TestImmutableList(unittest.TestCase):
    def test_size(self):
        self.assertEqual(size(None), 0)
        self.assertEqual(size(cons('a', None)), 1)
        self.assertEqual(size(cons('a', cons('b', None))), 2)

    def test_cons(self):
        self.assertEqual(cons('a', None), SingleNode('a', None))
        self.assertEqual(cons('a', cons('b', None)), SingleNode('a', SingleNode('b', None)))


    def test_remove(self):
        self.assertRaises(AssertionError, lambda: remove(None, 'a'))

        self.assertRaises(AssertionError, lambda: remove(cons('a', None), 'b'))
        self.assertEqual(remove(cons('a', cons('a', None)), 'a'), cons('a', None))
        self.assertEqual(remove(cons('a', cons('b', None)), 'a'), cons('b', None))
        self.assertEqual(remove(cons('a', cons('b', None)), 'b'), cons('a', None))

    def test_head(self):
        self.assertRaises(AssertionError, lambda: head(None))
        self.assertEqual(head(cons('a', None)), 'a')

    def test_tail(self):
        self.assertRaises(AssertionError, lambda: tail(None))

        self.assertEqual(tail(cons('a', None)), None)
        self.assertEqual(tail(cons('a', cons('b', None))), cons('b', None))

    def test_reverse(self):
        self.assertEqual(reverse(None), None)

        self.assertEqual(reverse(cons('a', None)), cons('a', None))
        self.assertEqual(reverse(cons('a', cons('b', None))), cons('b', cons('a', None)))

    def test_mconcat(self):
        self.assertEqual(mconcat(None, None), None)
        self.assertEqual(mconcat(cons('a', None), None), cons('a', None))
        self.assertEqual(mconcat(None, cons('a', None)), cons('a', None))
        self.assertEqual(mconcat(cons('a', None), cons('b', None)), cons('a', cons('b', None)))

    def test_to_list(self):
        self.assertEqual(to_list(None), [])

        self.assertEqual(to_list(cons('a', None)), ['a'])
        self.assertEqual(to_list(cons('a', cons('b', None))), ['a', 'b'])

    def test_from_list(self):
        test_data = [
                [],
                ['a'],
                ['a', 'b']
            ]

        for e in test_data:
            self.assertEqual(to_list(from_list(e)), e)

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        self.assertEqual(to_list(from_list(a)), a)

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst):
        a = from_list(lst)

        self.assertEqual(mconcat(mempty(), a), a)
        self.assertEqual(mconcat(a, mempty()), a)

    def test_iter(self):
        x = [1, 2, 3]

        lst = from_list(x)
        tmp = []
        try:
            get_next = iterator(lst)
            while True:
               tmp.append(get_next())
        except StopIteration:
            pass
        self.assertEqual(x, tmp)
        self.assertEqual(to_list(lst), tmp)
        get_next = iterator(None)
        self.assertRaises(StopIteration, lambda: get_next())


if __name__ == '__main__':
    unittest.main()
