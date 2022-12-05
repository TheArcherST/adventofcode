from fastaof import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            .. raw:: txt

                    [D]
                [N] [C]
                [Z] [M] [P]
                 1   2   3

                move 1 from 2 to 1
                move 3 from 1 to 3
                move 2 from 2 to 1
                move 1 from 1 to 2

        :output 1:
            .. raw:: txt

                CMZ

        """
        first, second = data.split("\n\n")

        lsts = []

        lines = first.split('\n')
        for i in lines:
            for nj, j in enumerate(i[1::4]):
                if j.isnumeric() or j == ' ':
                    continue
                while len(lsts) <= nj:
                    lsts.append([])
                lsts[nj].append(j)
        lsts = list(map(lambda x: list(reversed(x)), lsts))

        for i in second.split("\n"):
            if len(i) < 5: continue
            fromc, fromn, ton = map(int, i.split()[1::2])
            sel = lsts[fromn - 1]
            lsts[ton - 1] += reversed(sel[len(sel) - fromc:])
            for _ in range(fromc):
                lsts[fromn - 1].pop()

        res = ""

        for i in lsts:
            res += i[-1]

        return res

    def task_2(self, data):

        """Some task solution

        :input 1:
            .. raw:: txt

                    [D]
                [N] [C]
                [Z] [M] [P]
                 1   2   3

                move 1 from 2 to 1
                move 3 from 1 to 3
                move 2 from 2 to 1
                move 1 from 1 to 2

        :output 1:
            .. raw:: txt

                MCD

        """
        first, second = data.split("\n\n")
        lsts = []

        lines = first.split('\n')
        for i in lines:
            for nj, j in enumerate(i[1::4]):
                if j.isnumeric() or j == ' ':
                    continue
                while len(lsts) <= nj:
                    lsts.append([])
                lsts[nj].append(j)
        lsts = list(map(lambda x: list(reversed(x)), lsts))
        for i in second.split("\n"):
            if len(i) < 5:
                continue
            fromc, fromn, ton = map(int, i.split()[1::2])
            sel = lsts[fromn - 1]
            lsts[ton - 1] += sel[len(sel) - fromc:]
            for _ in range(fromc):
                lsts[fromn - 1].pop()

        res = ""

        for i in lsts:
            res += i[-1]

        return res
