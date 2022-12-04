from dataclasses import dataclass
from typing import Callable, List


@dataclass
class TestCase:
    input: str
    output: str


@dataclass
class TaskSolution:
    year: int
    day: int
    task_number: int
    func: Callable
    autotests: List[TestCase]
