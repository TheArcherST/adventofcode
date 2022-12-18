from fastaoc import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            2,2,2
            1,2,2
            3,2,2
            2,1,2
            2,3,2
            2,2,1
            2,2,3
            2,2,4
            2,2,6
            1,2,5
            3,2,5
            2,1,5
            2,3,5
        :output 1:
            64

        """
        seen = list()
        result = 0
        for i in data.strip().split('\n'):
            x, y, z = map(int, i.split(','))
            tp_coordinate = {(x, 0), (y, 1), (z, 2)}
            result += 6
            for j in seen:
                if len(j & tp_coordinate) == 2:
                    diff = j.symmetric_difference(tp_coordinate)
                    assert len(diff) == 2
                    a, b = diff
                    if abs(a[0] - b[0]) in range(0, 2):
                        result -= 2

            seen.append(tp_coordinate)
        return str(result)

