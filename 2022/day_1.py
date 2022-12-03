from fastaof import AdventOfCodePuzzle


def is_value_filter(seq):
    return filter(lambda _: bool(_), seq)


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):
        return max(map(lambda x: sum(map(int, is_value_filter(x.split('\n')))), data.split('\n\n')))

    def task_2(self, data):
        srt = sorted(map(lambda x: sum(map(int, is_value_filter(x.split('\n')))), data.split('\n\n')))
        return sum(srt[-3:])
