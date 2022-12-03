import datetime
import time

import requests
from rich.console import Console

from .models import TaskResolution


class SolutionExecutor:
    def __init__(self,
                 console: Console,
                 solution: TaskResolution,
                 session: str):

        self.console = console
        self.solution = solution
        self._session = session

    def run(self):
        """ Run workspace """

        self.console.print()

        with self.console.status('Input data loading...', spinner='bouncingBar'):
            self._load_input()

        task_indent = f'Task {self.solution.year}::{self.solution.day}::{self.solution.task_number}'
        section = f'============= {task_indent} ============='
        self.console.print(section)

        for n, testcase in enumerate(self.solution.autotests):
            actual_output = self.solution.func(self, testcase.input)

            if actual_output == testcase.output:
                self.console.print(f'Test {n + 1} [green]passed[/green]')
            else:
                self.console.print(f'[red]Test {n + 1} failed: [/red]{actual_output!r} != {testcase.output!r}')

        if self.solution.autotests:
            self.console.print('-' * len(section))

        start_at = time.monotonic_ns() / 1000
        try:
            result = self.solution.func(self, self._input_)
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

    def _input_url(self):
        return f'https://adventofcode.com/2022/day/{self.solution.day}/input'

    def _load_input(self):
        cookies = {
            'session': self._session
        }
        r = requests.get(self._input_url(), cookies=cookies)
        self._input_ = r.text
