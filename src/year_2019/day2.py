import logging
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle
from src.year_2019.intcode_computer import IntCodeComputer


class Day2(AdventOfCodePuzzle):

    def part_1(self, inputs: List[str]):
        program = [int(x) for x in inputs[0].split(',')]
        program[1] = 12
        program[2] = 2
        computer = IntCodeComputer(program)
        computer.run()
        return computer.memory[0]

    def part_2(self, inputs: List[str]):
        program = [int(x) for x in inputs[0].split(',')]

        for noun in range(100):
            for verb in range(100):
                test_program = program.copy()
                test_program[1] = noun
                test_program[2] = verb
                computer = IntCodeComputer(test_program, loglevel=logging.WARN)
                computer.run()
                if computer.memory[0] == 19690720:
                    return 100 * noun + verb
