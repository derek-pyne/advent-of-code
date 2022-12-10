from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class CathodeScreen:

    def __init__(self, instructions) -> None:
        self.x = self._parse_x_register(instructions)
        self.signal_strength = [val * (i + 1) for i, val in enumerate(self.x)]

    @staticmethod
    def _parse_x_register(instructions: List[str]):
        x = []
        x_current = 1
        for instruction in instructions:
            if instruction == 'noop':
                x.append(x_current)
            elif instruction.startswith('addx'):
                x.append(x_current)
                x.append(x_current)
                _, num = instruction.split()
                x_current += int(num)
        return x

    def draw(self, screen_width=40) -> str:
        output = ''
        for i, val in enumerate(self.x):
            draw_position = (i % 40)
            if abs(draw_position - val) < 2:
                output += '██'
            else:
                output += '  '

            if draw_position == screen_width - 1:
                output += '\n'
        return output


class Day10(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        c = CathodeScreen(instructions=inputs)
        return sum(c.signal_strength[19::40])

    def part_2(self, inputs: List[str]):
        c = CathodeScreen(instructions=inputs)
        print()
        print(c.draw())
        return 1
