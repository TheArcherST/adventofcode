from fastaof import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):
        """Some task solution

        :input 1:
            vJrwpWtwJgWrhcsFMMfFFhFp
            jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
            PmmdzqPrVvPwwTWBwg
            wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
            ttgJtRGJQctTZtZT
            CrZsJsPPZsGzwwsLwLmpwMDw
        :output 1:
            157

        """
        sum_ = 0
        for i in data.strip().split():
            a, b = i[len(i) // 2:], i[:len(i) // 2]
            lt = set(a) & set(b)
            for i in lt:
                if ord(i) in range(97, 123):
                    sum_ += ord(i) - 96
                else:
                    sum_ += ord(i) - 38
        return str(sum_)

    def task_2(self, data):
        """Some task solution

        :input 1:
            vJrwpWtwJgWrhcsFMMfFFhFp
            jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
            PmmdzqPrVvPwwTWBwg
            wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
            ttgJtRGJQctTZtZT
            CrZsJsPPZsGzwwsLwLmpwMDw
        :output 1:
            70

        """

        data = data.strip().split()
        literals = ''
        for i in range(0, len(data), 3):
            a, b, c = data[i:i+3]
            literals += (set(a) & set(b) & set(c)).pop()

        sum_ = 0
        for i in literals:
            if ord(i) in range(97, 123):
                sum_ += ord(i) - 96
            else:
                sum_ += ord(i) - 38
        return str(sum_)
