from typing import List
from typing import NewType


class SingleNode(object):
    def __init__(self, item, next=None):
        self.next = next
        self.item = item


class SingleLinkList(object):
    """单链表"""

    def __init__(self, head=None):
         self.head = head

    """初始化链表"""

    def initlist(self, data):
        self.head = SingleNode(data[0])

        p = self.head

        for i in data[1:]:
            node = SingleNode(i)
            p.next = node
            p = p.next

    def add(self, item):
        """头部添加元素"""
        # 先创建一个保存item值的节点
        node = SingleNode(item)
        # 将新节点的链接域next指向头节点，即_head指向的位置
        node.next = self.head
        # 将链表的头_head指向新节点
        self.head = node

    def append(self, item):
        """尾部添加元素"""
        node = SingleNode(item)
        # 先判断链表是否为空，若是空链表，则将_head指向新节点
        if self.is_empty():
            self.head = node
        # 若不为空，则找到尾部，将尾节点的next指向新节点
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = node

    def remove(self, item):
        """删除节点"""
        cur = self.head
        pre = None
        while cur != None:
            # 找到了指定元素
            if cur.item == item:
                # 如果第一个就是删除的节点
                if not pre:
                    # 将头指针指向头节点的后一个节点
                    self.head = cur.next
                else:
                    # 将删除位置前一个节点的next指向删除位置的后一个节点
                    pre.next = cur.next
                break
            else:
                # 继续按链表后移节点
                pre = cur
                cur = cur.next

    def length(self):
        """链表长度"""
        # cur初始时指向头节点
        cur = self.head
        count = 0
        # 尾节点指向None，当未到达尾部时
        while cur != None:
            count += 1
            # 将cur后移一个节点
            cur = cur.next
        return count

    def search(self, item):
        """链表查找节点位置，并返回位置或者False"""
        cur = self.head
        count = 0
        while cur.next is not None:
            if cur.item == item:
                return count
            cur = cur.next
            count += 1
        return False

    def map(self, f):
        cur = self.head
        while cur != None:
            cur.item = f(cur.item)
            cur = cur.next

    def reduce(self, f, initial_state):
        state = initial_state
        cur = self.head
        while cur != None:
            state = f(state, cur.item)
            cur = cur.next
        return state

    def is_empty(self):
        """判断链表是否为空"""
        return self.head == None

    def insert(self, pos, item):
        """指定位置添加元素"""
        # 若指定位置pos为第一个元素之前，则执行头部插入
        if pos <= 0:
            self.add(item)
        # 若指定位置超过链表尾部，则执行尾部插入
        elif pos > (self.length() - 1):
            self.append(item)
        # 找到指定位置
        else:
            node = SingleNode(item)
            count = 0
            # pre用来指向指定位置pos的前一个位置pos-1，初始从头节点开始移动到指定位置
            pre = self.head
            while count < (pos - 1):
                count += 1
                pre = pre.next
            # 先将新节点node的next指向插入位置的节点
            node.next = pre.next
            # 将插入位置的前一个节点的next指向新节点
            pre.next = node

    def travel(self):
        """遍历链表"""
        cur = self.head
        while cur != None:
            print(cur.item)
            cur = cur.next
        print("")

    def to_SingleLinkList(self):

        res = []
        cur = self.head
        while cur != None:
            res.append(cur.item)
            cur = cur.next
        return res

    def from_SingleLinkList(self, lst):
        if len(lst) == 0:
            self.head = None
            return
        head = None
        for e in reversed(lst):
            head = SingleNode(e, head)
        self.head = head


#  ----------------------------typing------------------
#一个典型的函数注释例子，为参数加上了类型
def greeting(name: SingleLinkList) -> SingleLinkList:
        return  name


def add_typing(a:int) -> SingleLinkList (List):
    list1 = list(range(a))
    return list1


# 类型别名(type alias)
Vector = SingleLinkList (float)

def scale(scalar: float, vector: Vector)->Vector:
    return [scalar*num for num in vector]


# New Type:  Use in test_add  function




import unittest

import hypothesis.strategies as st
from hypothesis import given


class TestMutableList(unittest.TestCase):


    def test_add(self):
        sllst = SingleLinkList()
        sllst.initlist([3])
        sllst.add(2)
        self.assertEqual(greeting(sllst.to_SingleLinkList()), ([2, 3]))
        sllst.add('b')
        self.assertEqual(sllst.to_SingleLinkList(), ['b', 2, 3])

        # New Type
        UserId = NewType("UserId", int)
        some_id = UserId(52)
        sllst.add(some_id)
        self.assertEqual(sllst.to_SingleLinkList(), [52,'b', 2, 3])

        UserId = NewType("UserId", str)
        some_id = UserId('aa')
        sllst.add(some_id)
        self.assertEqual(sllst.to_SingleLinkList(), ['aa',52, 'b', 2, 3])



    def test_append(self):
        sllst = SingleLinkList()
        sllst.append('a')
        self.assertEqual(greeting(sllst.to_SingleLinkList()), ['a'])
        sllst.append('b')
        self.assertEqual(sllst.to_SingleLinkList(), ['a', 'b'])

    def test_remove(self):
        sllst = SingleLinkList()
        sllst.initlist([3, 4, 5, 6])
        self.assertEqual(greeting(sllst.to_SingleLinkList()), [3, 4, 5, 6])
        sllst.remove(3)
        self.assertEqual(sllst.to_SingleLinkList(), [4, 5, 6])
        sllst.remove(4)
        self.assertEqual(sllst.to_SingleLinkList(), [5, 6])

    def test_Length(self):
        sllst = SingleLinkList()
        self.assertEqual(sllst.length(), 0)
        sllst.append('a')
        self.assertEqual(sllst.length(), 1)
        sllst.append('b')
        self.assertEqual(sllst.length(), 2)

    def test_search(self):
        sllst = SingleLinkList()
        sllst.initlist([3, 4, 5, 6])
        self.assertEqual(sllst.search(5), 2)
        self.assertEqual(sllst.search(3), 0)

    def test_map(self):
        sllst = SingleLinkList()
        sllst.map(str)
        sllst.initlist([1, 2, 6])
        sllst.map(str)
        self.assertEqual(sllst.to_SingleLinkList(), ["1", "2", "6"])

    def test_reduce(self):
        sllst = SingleLinkList()
        self.assertEqual(sllst.reduce(lambda st, e: st + e, 0), 0)

        sllst = SingleLinkList()
        sllst.initlist([1, 2, 3, 6])
        self.assertEqual(sllst.reduce(lambda st, e: st + e, 0), 12)

    def test_insert(self):
        sllst = SingleLinkList()
        sllst.insert(2, 'a')
        self.assertEqual(sllst.to_SingleLinkList(), ['a'])

        sllst = SingleLinkList()
        sllst.initlist([1, 2, 3])
        sllst.insert(2, 'a')
        self.assertEqual(sllst.to_SingleLinkList(), [1, 2, 'a', 3])

    def test_to_SingleLinkList(self):
        # //self.assertEqual(SingleLinkList().to_SingleLinkList(), ())
        self.assertEqual(SingleLinkList(SingleNode(1)).to_SingleLinkList(), [1])

    def test_from_SingleLinkList(self):
        test_data = [
            [],
            ['a'],
            ['a', 'b']
        ]
        for e in test_data:
            lst = SingleLinkList()
            lst.from_SingleLinkList(e)
            self.assertEqual(lst.to_SingleLinkList(), e)

    @given(st.lists(st.integers()))
    def test_from_SingleLinkList_to_SingleLinkList_equality(self, a):
        lst = SingleLinkList()
        lst.from_SingleLinkList(a)
        b = lst.to_SingleLinkList()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        lst = SingleLinkList()
        lst.from_SingleLinkList(a)
        self.assertEqual(lst.length(), len(a))

    def test_add_typing(self):
       self.assertEqual(add_typing(4), [0, 1, 2, 3])
       self.assertEqual(add_typing(5), [0, 1, 2, 3, 4])


    def test_type_alias(self):
        self.assertEqual(scale(2.0, [1.0, -4.2, 5.4]), [2.0, -8.4, 10.8])

if __name__ == '__main__':
    unittest.main()



