from __future__ import annotations

from fastaoc import AdventOfCodePuzzle
from dataclasses import dataclass
from typing import Union
from enum import Enum


class OperationType(Enum):
    DIV = 'DIV'
    MUL = 'MUL'
    ADD = 'ADD'
    SUB = 'SUB'
    CONST = 'CONST'


@dataclass
class Operation:
    key: str
    operation_type: OperationType
    args: tuple[Union[int, str], ...]

    def execute(self, op_dict: dict[str, Operation]):
        if self.operation_type is OperationType.CONST:
            return self.args[0]
        else:
            args = []
            for i in self.args:
                if isinstance(i, str):
                    args.append(op_dict[i].execute(op_dict))
                else:
                    args.append(i)

            first, second = args

            if self.operation_type is OperationType.SUB:
                return first - second
            elif self.operation_type is OperationType.ADD:
                return first + second
            elif self.operation_type is OperationType.DIV:
                return first / second
            elif self.operation_type is OperationType.MUL:
                return first * second
            else:
                raise KeyError(f"Can't execute operation with type {self.operation_type}")

    @classmethod
    def parse(cls, string: str) -> Operation:
        key, operation = string.split(': ')
        args: list[str] = operation.split()
        if len(args) == 1:
            return Operation(key, OperationType.CONST, (int(args[0]),))
        else:
            first, operator, second = args
            operator = {
                '*': OperationType.MUL,
                '/': OperationType.DIV,
                '-': OperationType.SUB,
                '+': OperationType.ADD
            }[operator]

            return Operation(key, operator, (first, second))

    def dependents(self) -> set[str]:
        if self.operation_type is OperationType.CONST:
            return set()
        else:
            return set(self.args)

    def recursive_dependents(self, op_dict):
        dependents = self.dependents()
        while dependents:
            current = dependents.pop()
            new = op_dict[current].dependents()
            yield from new
            dependents.update(new)

    def is_depend_from(self, op: Operation, op_dict):
        for i in self.recursive_dependents(op_dict):
            if i in op.key:
                return True
        else:
            return False

    def revert(self, mutable_operator_index, third):
        assert self.operation_type is not OperationType.CONST

        first, second = self.args

        if mutable_operator_index != 0:
            first, second = second, first

        op = {OperationType.ADD: OperationType.SUB,
              OperationType.SUB: OperationType.ADD,
              OperationType.DIV: OperationType.MUL,
              OperationType.MUL: OperationType.DIV}[self.operation_type]

        return Operation(self.key, op, (second, third))


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            root: pppw + sjmn
            dbpl: 5
            cczh: sllz + lgvd
            zczc: 2
            ptdq: humn - dvpt
            dvpt: 3
            lfqf: 4
            humn: 5
            ljgn: 2
            sjmn: drzm * dbpl
            sllz: 4
            pppw: cczh / lfqf
            lgvd: ljgn * ptdq
            drzm: hmdt - zczc
            hmdt: 32
        :output 1:
            152

        """

        ops = dict()
        root = None

        for i in data.strip().split('\n'):
            op = Operation.parse(i)
            ops.update({op.key: op})
            if op.key == 'root':
                root = op

        return str(root.execute(ops))

    def task_2(self, data):

        """Some task solution

        :input 1:
            root: pppw + sjmn
            dbpl: 5
            cczh: sllz + lgvd
            zczc: 2
            ptdq: humn - dvpt
            dvpt: 3
            lfqf: 4
            humn: 5
            ljgn: 2
            sjmn: drzm * dbpl
            sllz: 4
            pppw: cczh / lfqf
            lgvd: ljgn * ptdq
            drzm: hmdt - zczc
            hmdt: 32
        :output 1:
            301

        """

        ops = dict()
        root = None
        me = None

        for i in data.strip().split('\n'):
            op = Operation.parse(i)
            ops.update({op.key: op})
            if op.key == 'root':
                root = op
            elif op.key == 'humn':
                me = op

        first, second = ops[root.args[0]], ops[root.args[1]]

        while True:
            if first.is_depend_from(me, ops):
                mutable = first
                immutable = second
            elif second.is_depend_from(me, ops):
                mutable = second
                immutable = first
            else:
                raise RuntimeError()

            current_excepted = immutable.execute(ops)

            if ops[mutable.args[0]].is_depend_from(me, ops):
                index = 0
            else:
                index = 1

            reverted = mutable.revert(index, current_excepted)
            current_excepted = reverted.execute(ops)

            # ops[mutable.key] = mutable

            mut_gen = ops[mutable.args[index]]

            if mut_gen.operation_type is OperationType.CONST:
                break

            first, second = ops[mut_gen.args[0]], ops[mut_gen.args[1]]

        me.revert()
        while mutable.execute(ops) != constant:
            me.args[0] += 1
        return str(me.args[0])
