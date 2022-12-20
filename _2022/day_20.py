from typing import Iterable, TypeVar

from fastaoc import AdventOfCodePuzzle


T = TypeVar('T')


class MySequence:
    def __init__(self, sequence: Iterable[int]):
        # PyCharm TypeChecker bug...
        # noinspection PyTypeChecker
        self.indexed_sequence: list[tuple[int, int]] = list(enumerate(sequence))

    @property
    def sequence(self) -> list[int]:
        return [i[1] for i in self.indexed_sequence]

    def __getitem__(self, other):
        return self.indexed_sequence[self.resolve_index(other, to_insert=False)]

    def __setitem__(self, n, o):
        self.indexed_sequence[self.resolve_index(n)] = o

    def resolve_index(self, other, to_insert=True, sus_behavior=False):
        a = ((abs(other) + (abs(other) // len(self.indexed_sequence) if to_insert else 0)) % (
                    len(self.indexed_sequence) - (1 if sus_behavior else 0)))
        if other < 0:
            a = -a
        if (not a) and to_insert:
            a = len(self.indexed_sequence)
        # print(f'Index resolve: {other} -> {a}')

        return a

    def resolve(self, times=1, sus_index_behavior: bool = False):
        indexed_list = list(enumerate(self.indexed_sequence))

        for _ in range(times):
            for (n, i) in enumerate(sorted(indexed_list.copy(), key=lambda x: x[0])):
                # print([i[1] for i in indexed_list])
                actual_index = indexed_list.index(i)
                e = indexed_list.pop(actual_index)
                # print(f'Pop element {e} from list')
                new_index = self.resolve_index(actual_index + i[1][1], to_insert=False, sus_behavior=sus_index_behavior)
                # print(f'Index to insert is {new_index}')
                indexed_list.insert(new_index, i)
                # print(f'Insert value {i} for index {new_index}')
                # print('======' * 10)
                # print([i[1] for i in indexed_list])

        self.indexed_sequence = [i[1] for i in indexed_list]

        # self.sequence = list(i[1] for i in indexed_list)


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

        seq = MySequence(map(int, data.strip().split()))
        seq.resolve()

        zi = seq.sequence.index(0)

        return str(seq[zi + 1000][1] + seq[zi + 2000][1] + seq[zi + 3000][1])

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

        seq = MySequence(map(lambda x: int(x) * 811589153, data.strip().split()))

        seq.resolve(10, sus_index_behavior=True)

        zi = seq.sequence.index(0)

        return str(seq[zi + 1000][1] + seq[zi + 2000][1] + seq[zi + 3000][1])
