from typing import Iterable, TypeVar
from enum import Enum

from fastaoc import AdventOfCodePuzzle


T = TypeVar('T')


class IndexationBehavior(Enum):
    FIRST = 'FIRST'
    SECOND = 'SECOND'


class MySequence:
    def __init__(self, sequence: Iterable[int], indexation_behaviour: IndexationBehavior):
        # PyCharm TypeChecker bug...
        # noinspection PyTypeChecker
        self.indexed_sequence: list[tuple[int, int]] = list(enumerate(sequence))
        self.indexation_behaviour = indexation_behaviour
        self.length = len(self.indexed_sequence)

    @property
    def sequence(self) -> list[int]:
        return [i[1] for i in self.indexed_sequence]

    def __getitem__(self, other):
        return self.indexed_sequence[self.resolve_index(other, getter=True)]

    def __setitem__(self, n, o):
        self.indexed_sequence[self.resolve_index(n)] = o

    def resolve_index(self, other, behaviour: IndexationBehavior = None, getter: bool = False):
        behaviour = behaviour or self.indexation_behaviour

        if behaviour is IndexationBehavior.FIRST:
            if not other:
                index = len(self.indexed_sequence)
            else:
                if getter:
                    index = abs(other) % self.length
                else:
                    index = (abs(other) + (abs(other) // self.length)) % self.length

        elif self.indexation_behaviour is IndexationBehavior.SECOND:
            if not other:
                print('y')
                index = len(self.indexed_sequence)
            else:
                if getter:
                    index = (other % (self.length - 1))
                else:
                    index = ((other + (abs(other) // self.length)) % (self.length - 1))
        else:
            raise RuntimeError()

        if other < 0:
            index = -index

        return index

    def resolve(self, times=1):
        indexed_list = list(enumerate(self.indexed_sequence))

        for _ in range(times):
            for (n, i) in enumerate(sorted(indexed_list.copy(), key=lambda x: x[0])):
                actual_index = indexed_list.index(i)
                indexed_list.pop(actual_index)
                new_index = self.resolve_index(actual_index + i[1][1])
                indexed_list.insert(new_index, i)

        self.indexed_sequence = [i[1] for i in indexed_list]


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):
        """Some task solution

        :input 1:
            1
            2
            -3
            3
            -2
            0
            4
        :output 1:
            3

        """

        seq = MySequence(map(int, data.strip().split()), IndexationBehavior.FIRST)
        seq.resolve()

        zero_index = seq.sequence.index(0)
        return str(seq[zero_index + 1000][1] + seq[zero_index + 2000][1] + seq[zero_index + 3000][1])

    def task_2(self, data):
        """Some task solution

        :input 1:
            1
            2
            -3
            3
            -2
            0
            4
        :output 1:
            1623178306

        """

        seq = MySequence(map(lambda x: int(x) * 811589153, data.strip().split()), IndexationBehavior.SECOND)

        seq.resolve(10)
        zero_index = seq.sequence.index(0)

        return str(seq[zero_index + 1000][1] + seq[zero_index + 2000][1] + seq[zero_index + 3000][1])
