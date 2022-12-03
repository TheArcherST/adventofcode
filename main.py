import dotenv
from rich.console import Console

from fastaof import AdventOfCodePuzzle, ResolutionExecutor
from fastaof.structure import load_modules


def main():
    data = dotenv.dotenv_values()
    console = Console()

    load_modules()
    latest = AdventOfCodePuzzle.get_latest()
    executor = ResolutionExecutor(console, latest, data['SESSION'])
    executor.run()


if __name__ == '__main__':
    main()
