from itertools import islice
from enum import Enum

from base import AdventOfCodeWorkspace


class GameEnum(Enum):
    PAPER = 'PAPER'
    ROCK = 'ROCK'
    SCISSORS = 'SCISSORS'

    @classmethod
    def to_score(cls, val):
        lib = {cls.ROCK: 1,
               cls.PAPER: 2,
               cls.SCISSORS: 3}

        return lib[val]

    @classmethod
    def to_win(cls, val):
        # note: normalize(val + 1)
        lib = {cls.ROCK: cls.PAPER,
               cls.PAPER: cls.SCISSORS,
               cls.SCISSORS: cls.ROCK}

        return lib[val]

    @classmethod
    def to_lose(cls, val):
        # note: normalize(val + 2)
        lib = {cls.ROCK: cls.SCISSORS,
               cls.PAPER: cls.ROCK,
               cls.SCISSORS: cls.PAPER}

        return lib[val]


def batched(iterable, n):
    if n < 1:
        raise ValueError('n must be >= 1')

    it = iter(iterable)

    while batch := list(islice(it, n)):
        yield batch


def is_value_filter(seq):
    return filter(lambda _: bool(_), seq)


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


class Resolution(AdventOfCodeWorkspace):
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
