from enum import Enum

from fastaof import AdventOfCodePuzzle


class GameEnum(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def to_score(cls, val):
        lib = {cls.ROCK: 1,
               cls.PAPER: 2,
               cls.SCISSORS: 3}

        return lib[val]

    @staticmethod
    def normalize(n: int):  # depend from number 3
        return ((n - 1) % 3) + 1

    @classmethod
    def to_win(cls, val: 'GameEnum'):
        res = GameEnum(cls.normalize(val.value+1))
        return res

    @classmethod
    def to_lose(cls, val: 'GameEnum'):
        res = GameEnum(cls.normalize(val.value+2))
        return res


def prepare_literal(l):
    lib = {
        'A': GameEnum.ROCK,
        'B': GameEnum.PAPER,
        'C': GameEnum.SCISSORS,
        'X': GameEnum.ROCK,
        'Y': GameEnum.PAPER,
        'Z': GameEnum.SCISSORS
    }

    return lib[l]


class Resolution(AdventOfCodePuzzle):
    def task_1(self, data):
        data = data.strip()
        score = 0
        for i in data.split('\n'):
            a, b = map(prepare_literal, i.split())
            score += GameEnum.to_score(b)
            if a is b:
                score += 3
            elif any([a is GameEnum.SCISSORS and b is GameEnum.ROCK,
                      a is GameEnum.ROCK and b is GameEnum.PAPER,
                      a is GameEnum.PAPER and b is GameEnum.SCISSORS]):
                score += 6

            else:
                pass
        return score

    def task_2(self, data):
        data = data.strip()
        score = 0
        for i in data.split('\n'):
            first, second = i.split()
            a = prepare_literal(first)

            if second == 'X':
                b = GameEnum.to_lose(a)
            elif second == 'Y':
                b = a
            else:
                b = GameEnum.to_win(a)

            score += GameEnum.to_score(b)
            if a is b:
                score += 3
            elif GameEnum.to_win(a) is b:
                score += 6

            else:
                pass
        return score
