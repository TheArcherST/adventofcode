import os

import dotenv
from rich.console import Console

from fastaoc import AdventOfCodePuzzle, SolutionExecutor
from fastaoc.structure import load_modules


def main():
    dotenv.load_dotenv()

    console = Console()

    load_modules()
    latest = AdventOfCodePuzzle.get_latest()
    executor = SolutionExecutor(console, latest, os.environ['ADVENT_OF_CODE_SESSION'])
    executor.run()


if __name__ == '__main__':
    main()
