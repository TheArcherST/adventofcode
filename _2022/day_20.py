from fastaoc import AdventOfCodePuzzle


class MySeq:
    def __init__(self, seq):
        self.seq = list(seq)

    def __getitem__(self, other):
        return self.seq[self.resolve_index(other, to_insert=False)]

    def __setitem__(self, n, o):
        self.seq[self.resolve_index(n)] = o

    def resolve_index(self, other, to_insert=True):
        a = ((abs(other) + (abs(other) // len(self.seq) if to_insert else 0)) % (len(self.seq)))
        if other < 0:
            a = -a
        if (not a) and to_insert:
            return len(self.seq)
        else:
            return a
        # print(f'Index resolve: {other} -> {a}')

    def resolve(self):
        indexed_list = list(enumerate(self.seq))

        for n, i in enumerate(indexed_list.copy()):
            # print(f'Current sequence: {[i[1] for i in indexed_list]}')
            actual_index = indexed_list.index(i)
            indexed_list.pop(actual_index)
            # print(f'Pop element {element} from list')
            index = self.resolve_index(actual_index + i[1])
            # print(f'Index to insert is {index}')
            indexed_list.insert(index, i)
            # print(f'Insert value {i} for index {index}')
            # print('======' * 10)

        # print(f'Final sequence: {[i[1] for i in indexed_list]}')

        self.seq = list(i[1] for i in indexed_list)


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

        seq = MySeq(map(int, data.strip().split()))
        seq.resolve()

        zi = seq.seq.index(0)
        return str(seq[zi + 1000] + seq[zi + 2000] + seq[zi + 3000])

    def task_0(self, data):
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

        seq = MySeq(map(lambda x: int(x) * 811589153, data.strip().split()))

        for i in range(10):
            seq.resolve()

        zi = seq.seq.index(0)
        return str(seq[zi + 1000] + seq[zi + 2000] + seq[zi + 3000])
