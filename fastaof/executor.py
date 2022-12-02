import time
import datetime

import requests
from rich.console import Console

from .models import TaskResolution


class ResolutionExecutor:
    def __init__(self,
                 console: Console,
                 resolution: TaskResolution,
                 session: str):

        self.console = console
        self.resolution = resolution
        self._session = session

    def run(self):
        """ Run workspace """

        with self.console.status('Input data loading...', spinner='bouncingBar'):
            self._load_input()

        self.console.print(f'Processing task {self.resolution.year}.'
                           f'{self.resolution.day}::{self.resolution.task_number}',
                           end='\n\n')

        task_indent = f'Task {self.resolution.year}::{self.resolution.day}::{self.resolution.task_number}'
        section = f'============= {task_indent} ============='
        self.console.print(section)

        for n, testcase in enumerate(self.resolution.autotests):
            actual_output = self.resolution.func(self, testcase.input)

            if actual_output == testcase.output:
                self.console.print(f'Test {n + 1} [green]passed[/green]')
            else:
                self.console.print(f'[red]Test {n + 1} failed: [/red]{actual_output!r} != {testcase.output!r}')

        if self.resolution.autotests:
            self.console.print('-' * len(section))

        start_at = time.monotonic_ns() / 1000
        try:
            result = self.resolution.func(self, self._input_)
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
        return f'https://adventofcode.com/2022/day/{self.resolution.day}/input'

    def _load_input(self):
        cookies = {
            'session': self._session
        }
        r = requests.get(self._input_url(), cookies=cookies)
        self._input_ = r.text
