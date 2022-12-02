import datetime
import time

from dataclasses import dataclass
from typing import Callable, Type, List, Dict
from hashlib import md5
from pytest import fixture
from rich.console import Console

import requests


@fixture
def data() -> str:
    pass


@dataclass
class TaskResolution:
    day: int
    task_number: int
    func: Callable


@dataclass
class Testcase:
    input: str
    output: str


@dataclass
class ResolutionTests:
    cases: Dict[str, List[Testcase]]


class AdventOfCodeWorkspace:
    """AdventOfCodeWorkspace class

    Is workspace to fastly resolve advent of code tasks

    """

    _input_: str = None
    _resolutions_: list[TaskResolution] = []
    _day_ = None
    _workspaces_: list[Type['AdventOfCodeWorkspace']] = []

    @classmethod
    def get_day(cls):
        return cls._day_

    def __init__(self, console: Console, tests: ResolutionTests, session_token: str):
        self.console = console
        self.tests = tests

        self._session = session_token

    def _input_url(self):
        return f'https://adventofcode.com/2022/day/{self._day_}/input'

    def _load_input(self):
        cookies = {
            'session': self._session
        }
        r = requests.get(self._input_url(), cookies=cookies)
        self._input_ = r.text

    def __init_subclass__(cls, **kwargs):
        """ Register all resolutions in cls """

        cls._workspaces_.append(cls)
        cls._resolutions_ = []

        for k, v in cls.__dict__.items():
            if k.startswith('task_'):
                number = int(k.removeprefix('task_'))
                resolution = TaskResolution(cls._day_,
                                            number,
                                            v)
                cls._resolutions_.append(resolution)

    def execute_case(self, case: Testcase):
        pass

    def run(self):
        """ Run workspace """

        self.console.print(f'Processing day {self._day_}', end='\n\n')

        with self.console.status('Input data loading...', spinner='bouncingBar'):
            self._load_input()

        self.console.print(f'Input data hash: {md5(self._input_.encode("utf-8")).hexdigest()}', end='\n\n')

        for i in self._resolutions_:
            section = f'======= Task {i.task_number} ======='
            self.console.print(section)

            testcases = self.tests.cases.get(i.func.__name__, [])

            for n, testcase in enumerate(testcases):
                result = str(i.func(self, testcase.input))
                if result == testcase.output:
                    self.console.print(f'Test {n+1} [green]passed[/green]')
                else:
                    self.console.print(f'[red]Test {n+1} failed: [/red]{result!r} != {testcase.output!r}')

            if testcases:
                self.console.print('-' * len(section))

            start_at = time.monotonic_ns() / 1000
            try:
                result = i.func(self, self._input_)
            except Exception as e:
                self.console.print(f'Error: {e}')
            else:
                self.console.print(f'Result: {result}')
            finally:
                elapsed_ns = time.monotonic_ns() / 1000 - start_at
                elapsed = datetime.timedelta(microseconds=elapsed_ns)
                self.console.print(f'Time elapsed: {elapsed.total_seconds()}s')

            self.console.print('=' * len(section))
            self.console.print()

        self.console.print()

    @classmethod
    def get_latest_day(cls) -> int:
        dct = {i._day_: i for i in cls._workspaces_}
        latest_day = max(dct.keys())
        return latest_day

    @classmethod
    def find_by_day(cls, day: int):
        for i in cls._workspaces_:
            if i._day_ == day:
                return i
        else:
            raise KeyError(f"Workspace for day {day} not found")
