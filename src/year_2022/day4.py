import re
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Pair:

    def __init__(self, elf1_start: int, elf1_end: int, elf2_start: int, elf2_end: int) -> None:
        self.elf1 = [elf1_start, elf1_end]
        self.elf2 = [elf2_start, elf2_end]

    def is_fully_overlap(self) -> bool:
        if (self.elf1[0] <= self.elf2[0]) and (self.elf1[1] >= self.elf2[1]):
            return True
        elif (self.elf2[0] <= self.elf1[0]) and (self.elf2[1] >= self.elf1[1]):
            return True
        else:
            return False

    def is_any_overlap(self) -> bool:
        if self.elf1[0] <= self.elf2[0] <= self.elf1[1]:
            return True
        elif self.elf1[0] <= self.elf2[1] <= self.elf1[1]:
            return True
        if self.elf2[0] <= self.elf1[0] <= self.elf2[1]:
            return True
        elif self.elf2[0] <= self.elf1[1] <= self.elf2[1]:
            return True
        else:
            return False


def get_pairs(inputs: List[str]) -> List[Pair]:
    pairs = []
    for line in inputs:

        match = re.match('(\d*)-(\d*),(\d*)-(\d*)', line)
        if not match:
            raise ValueError(f'Failed to parse: {line}')
        pairs.append(Pair(
            elf1_start=int(match.groups()[0]),
            elf1_end=int(match.groups()[1]),
            elf2_start=int(match.groups()[2]),
            elf2_end=int(match.groups()[3]),
        ))
    return pairs


class Day4(AdventOfCodePuzzle):

    def part_1(self, inputs: List[str]) -> int:
        pairs = get_pairs(inputs=inputs)
        return sum([pair.is_fully_overlap() for pair in pairs])

    def part_2(self, inputs: List[str]) -> int:
        pairs = get_pairs(inputs=inputs)
        return sum([pair.is_any_overlap() for pair in pairs])
