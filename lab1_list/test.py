import typing
from typing import List, Tuple, Dict

from linkList import SingleLinkList


def add(a:int) -> SingleLinkList (List):
    list1 = list(range(a))

    return list1
print(add(5))
# 结果：([0, 1, 2, 3, 4], ('hhhh', 'hhhh', 'hhhh'), {'a': 2.3}, False)




Vector = SingleLinkList (float)

def scale(scalar: float, vector: Vector)->Vector:
    return [scalar*num for num in vector]

new_vector = scale(2.0, [1.0, -4.2, 5.4])


from typing import NewType

UserId = NewType("UserId", int)
some_id = UserId(524313)
print(some_id)



