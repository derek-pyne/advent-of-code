from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Day1(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        sum = 0
        for line in inputs:
            sum += int(line) // 3 - 2
        return sum

    def part_2(self, inputs: List[str]):
        sum = 0
        for line in inputs:
            fuel = int(line)
            while fuel > 0:
                fuel = fuel // 3 - 2
                sum += max(fuel, 0)
        return sum
