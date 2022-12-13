from fastaoc import AdventOfCodePuzzle
from ast import literal_eval
from typing import Iterable, Union, Sized


def compare(left_list: Union[int, Union[Iterable[int], Sized]],
            right_list: Union[int, Union[Iterable[int], Sized]]):

    if isinstance(left_list, int):
        left_list = [left_list]
    if isinstance(right_list, int):
        right_list = [right_list]

    for left, right in zip(left_list, right_list):
        if isinstance(left, Iterable) or isinstance(right, Iterable):
            comp_result = compare(left, right)
            if isinstance(comp_result, bool):
                return comp_result
            else:
                continue

        if left > right:
            return False
        elif left < right:
            return True
        else:
            continue

    if len(left_list) > len(right_list):
        return False
    elif len(left_list) < len(right_list):
        return True
    else:
        return None


def add_element_to_sorted_list(element, lst: list):
    for n, i in enumerate(lst):
        if compare(element, i):
            lst.insert(n, element)
            break
    else:
        lst.append(element)


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):
        """Some task solution

        :input 1:
            [1,1,3,1,1]
            [1,1,5,1,1]

            [[1],[2,3,4]]
            [[1],4]

            [9]
            [[8,7,6]]

            [[4,4],4,4]
            [[4,4],4,4,4]

            [7,7,7,7]
            [7,7,7]

            []
            [3]

            [[[]]]
            [[]]

            [1,[2,[3,[4,[5,6,7]]]],8,9]
            [1,[2,[3,[4,[5,6,0]]]],8,9]
        :output 1:
            13

        """

        result = 0

        for n, p in enumerate(data.strip().split("\n\n")):
            lst = list(map(literal_eval, p.split("\n")))
            if compare(*lst):
                result += n + 1
            else:
                pass

        return str(result)

    def task_2(self, data):
        """Some task solution

        :input 1:
            [1,1,3,1,1]
            [1,1,5,1,1]

            [[1],[2,3,4]]
            [[1],4]

            [9]
            [[8,7,6]]

            [[4,4],4,4]
            [[4,4],4,4,4]

            [7,7,7,7]
            [7,7,7]

            []
            [3]

            [[[]]]
            [[]]

            [1,[2,[3,[4,[5,6,7]]]],8,9]
            [1,[2,[3,[4,[5,6,0]]]],8,9]
        :output 1:
            140

        """

        sorted_list = []

        for n, p in enumerate(['[[2]]\n[[6]]'] + list(data.strip().split("\n\n"))):
            lst = list(map(literal_eval, p.split("\n")))

            for i in lst:
                add_element_to_sorted_list(i, sorted_list)

        result = (sorted_list.index([[2]]) + 1) * (sorted_list.index([[6]]) + 1)
        return str(result)
