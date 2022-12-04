from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Day2(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        h_pos = 0
        depth = 0

        for line in inputs:
            command, num = line.split()
            num = int(num)
            if command == 'down':
                depth += num
            elif command == 'up':
                depth -= num
            elif command == 'forward':
                h_pos += num
            else:
                raise ValueError(f'Weird command: {command}')

        return h_pos * depth

    def part_2(self, inputs: List[str]) -> int:
        h_pos = 0
        depth = 0
        aim = 0

        for line in inputs:
            command, num = line.split()
            num = int(num)
            if command == 'down':
                aim += num
            elif command == 'up':
                aim -= num
            elif command == 'forward':
                h_pos += num
                depth += aim * num
            else:
                raise ValueError(f'Weird command: {command}')

        return h_pos * depth
