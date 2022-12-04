from typing import List

import pandas as pd

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Day1(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        readings = pd.Series([int(line) for line in inputs])
        diffs = readings > readings.shift(1)
        return diffs.sum()

    def part_2(self, inputs: List[str]) -> int:
        readings = pd.Series([int(line) for line in inputs])
        rolling_sum = readings.rolling(window=3).sum()
        diffs = rolling_sum > rolling_sum.shift(1)
        return diffs.sum()
