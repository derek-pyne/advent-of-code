from collections import Counter
from itertools import accumulate
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Day1(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        c = Counter(inputs[0])
        return c['('] - c[')']

    def part_2(self, inputs: List[str]) -> int:
        i = [1 if n == '(' else -1 for n in inputs[0]]
        floors = list(accumulate(i))
        is_basement = [f < 0 for f in floors]
        return is_basement.index(True) + 1
