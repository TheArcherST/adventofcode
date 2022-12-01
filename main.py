import os

import importlib
from base import AdventOfCodeWorkspace
import re


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


def main():
    load_modules()
    latest = AdventOfCodeWorkspace.find_latest()
    latest = latest()
    latest.run()


if __name__ == '__main__':
    main()
