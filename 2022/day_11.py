import pprint

from fastaoc import AdventOfCodePuzzle
import yaml
from dataclasses import dataclass


class Operation:
    def __init__(self, string: str):
        self.string = string

    def exec(self, number: float) -> float:
        return eval(self.string, {'old': number})

    def __str__(self):
        return repr(self.string)

    __repr__ = __str__


class Test:
    def __init__(self, string: str):
        self.string = string

    @property
    def div_by(self):
        if self.string.startswith('divisible by '):
            return int(self.string.split('by ')[1])
        else:
            raise NotImplementedError

    def exec(self, number: float) -> float:
        return number % self.div_by == 0

    def __str__(self):
        return repr(self.string)

    __repr__ = __str__


class MyNumber:
    def __init__(self, initial: float):
        self.initial = initial
        self.operations: list[Operation] = []

    def add_operation(self, op: Operation):
        self.operations.append(op)


@dataclass
class Monkey:
    items: list[int]
    operation: Operation
    test: Test
    if_true: int
    if_false: int

    total_inspected: int = 0


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
        :output 1:

        """
        monkeys: dict[int, Monkey] = dict()
        iterator = iter(data.strip().split('\n'))
        while True:
            try:
                curr = ''
                while not curr:
                    curr = next(iterator)
            except StopIteration:
                break

            monkeys.update(
                {
                    int(curr.split()[1][:-1]): Monkey(
                        list(map(int, next(iterator).replace('  Starting items: ', '').split(', '))),
                        Operation(next(iterator).replace('  Operation: new = ', '')),
                        Test(next(iterator).replace('  Test: ', '')),
                        int(next(iterator).replace('    If true: throw to monkey ', '')),
                        int(next(iterator).replace('    If false: throw to monkey ', ''))
                    )}
            )

        rounds = 20
        for _ in range(rounds):
            for n, i in monkeys.items():
                items = i.items.copy()
                i.items.clear()

                for j in items:
                    actual_j = int(i.operation.exec(j) / 3)
                    if i.test.exec(actual_j):
                        monkeys[i.if_true].items.append(actual_j)
                    else:
                        monkeys[i.if_false].items.append(actual_j)

                i.total_inspected += len(items)

        most_active = sorted(monkeys.values(), key=lambda x: x.total_inspected)[-2:]
        business = 1
        for i in most_active:
            business *= i.total_inspected

        return business

    def task_2(self, data):

        """Some task solution

        :input 1:
        :output 1:

        """

        test_period = 1

        monkeys: dict[int, Monkey] = dict()
        iterator = iter(data.strip().split('\n'))
        while True:
            try:
                curr = ''
                while not curr:
                    curr = next(iterator)
            except StopIteration:
                break

            monkeys.update(
                {
                    int(curr.split()[1][:-1]): Monkey(
                        list(map(int, next(iterator).replace('  Starting items: ', '').split(', '))),
                        Operation(next(iterator).replace('  Operation: new = ', '')),
                        Test(next(iterator).replace('  Test: ', '')),
                        int(next(iterator).replace('    If true: throw to monkey ', '')),
                        int(next(iterator).replace('    If false: throw to monkey ', ''))
                    )}
            )

        for i in monkeys.values():
            test_period *= i.test.div_by

        rounds = 10000
        for _ in range(rounds):
            print(_)
            for n, i in monkeys.items():
                items = i.items.copy()
                i.items.clear()

                for j in items:
                    actual_j = int(i.operation.exec(j)) % test_period
                    if i.test.exec(actual_j):
                        monkeys[i.if_true].items.append(actual_j)
                    else:
                        monkeys[i.if_false].items.append(actual_j)

                i.total_inspected += len(items)

        most_active = sorted(monkeys.values(), key=lambda x: x.total_inspected)[-2:]
        business = 1
        for i in most_active:
            business *= i.total_inspected

        return business
