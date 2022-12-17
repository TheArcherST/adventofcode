import importlib
import os
import re


def load_modules():
    for i in os.listdir('.'):

        if not re.fullmatch(r'^_[0-9]+$', i):
            continue

        year = int(i[1:])

        for j in os.listdir(i):
            if not re.fullmatch(r'day_[0-9]+[.]py', j):
                continue

            day = int(j.removeprefix('day_').removesuffix('.py'))

            module_name = f'{i}.' + j.removesuffix('.py')

            try:
                module = importlib.import_module(module_name)

                if hasattr(module, 'Solution'):
                    module.Solution.__year__ = year
                    module.Solution.__day__ = day

                    module.Solution.register_solutions()

                else:
                    print(f"Can't find `Solution` class in {i!r} file")

            except ImportError as e:
                raise ImportError(f"Can't import module {module_name}") from e
