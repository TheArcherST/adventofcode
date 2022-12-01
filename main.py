import os

import importlib
import re
import yaml
import dotenv

from base import AdventOfCodeWorkspace, ResolutionTests
from rich.console import Console

from dataclass_factory import Factory


def load_modules(root_module: str = r'resolutions'):
    for i in os.listdir(root_module):
        if not re.fullmatch(r'day_[0-9]+[.]py', i):
            continue

        day = int(i.removeprefix('day_').removesuffix('.py'))

        try:
            module = importlib.import_module('resolutions.' + i.removesuffix('.py'))

            if hasattr(module, 'Resolution'):
                module.Resolution._day_ = day
            else:
                print(f"Can't find resolution in {i!r} file")

        except ImportError:
            print(f"Can't import module {i}")


def load_testcases(day: int) -> ResolutionTests:
    with open(f'testcases/day_{day}.yaml') as fs:
        data = yaml.safe_load(fs)

    factory = Factory()
    tests = factory.load(data, ResolutionTests)

    return tests


def main():
    data = dotenv.dotenv_values()
    console = Console()

    load_modules()
    day = AdventOfCodeWorkspace.get_latest_day()
    latest = AdventOfCodeWorkspace.find_by_day(day)
    testcases = load_testcases(day)

    latest = latest(console, testcases, data['SESSION'])
    latest.run()


if __name__ == '__main__':
    main()
