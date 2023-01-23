from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle
from src.year_2019.intcode_computer import IntCodeComputer


class Day5(AdventOfCodePuzzle):

    def part_1(self, inputs: List[str]):
        program = [int(x) for x in inputs[0].split(',')]
        computer = IntCodeComputer(program)
        return computer.run(input=1)

    def part_2(self, inputs: List[str]):
        program = [int(x) for x in inputs[0].split(',')]
        computer = IntCodeComputer(program)
        return computer.run(input=5)
