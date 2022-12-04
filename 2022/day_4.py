from fastaof import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task resolution

        :input 1:
            2-4,6-8
            2-3,4-5
            5-7,7-9
            2-8,3-7
            6-6,4-6
            2-6,4-8
        :output 1:
            4

        """

        data = data.strip()
        res = 0
        for i in data.split('\n'):
            a, b = i.split(',')
            a1, a2 = a.split('-')
            b1, b2 = b.split('-')
            range1 = range(int(a1), int(a2) + 1)
            range2 = range(int(b1), int(b2) + 1)
            il = len(set(range1) & set(range2))
            if il:
                res += 1
        return str(res)
