import os

import dotenv
from rich.console import Console

from fastaof import AdventOfCodePuzzle, ResolutionExecutor
from fastaof.structure import load_modules


def main():
    dotenv.load_dotenv()

    console = Console()

    load_modules()
    latest = AdventOfCodePuzzle.get_latest()
    executor = ResolutionExecutor(console, latest, os.environ['ADVENT_OF_CODE_SESSION'])
    executor.run()


if __name__ == '__main__':
    main()
