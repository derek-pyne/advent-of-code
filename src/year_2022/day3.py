from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle
from src.utils import grouper


class Backpack:

    def __init__(self, raw_input: str) -> None:
        parsed_line = [c for c in raw_input.strip()]
        self.all = set(parsed_line)
        self.first_comp = set(parsed_line[:int(len(parsed_line) / 2)])
        self.second_comp = set(parsed_line[int(len(parsed_line) / 2):])
        self.common_item = self._get_common_item()
        self.common_priority = self.get_item_priority(self.common_item)

    def _get_common_item(self):
        common = self.first_comp.intersection(self.second_comp)
        if len(common) != 1:
            raise ValueError('Not one thing in common between compartments')

        return common.pop()

    @staticmethod
    def get_item_priority(item: str) -> int:
        if item.islower():
            ref_letter = 'a'
            shift = 1
        else:
            ref_letter = 'A'
            shift = 27

        return ord(item) - ord(ref_letter) + shift

    @staticmethod
    def find_common_item_with_backpacks(backpacks):
        common = backpacks[0].all
        for b in backpacks[1:]:
            common = common.intersection(b.all)
        if len(common) != 1:
            raise ValueError('Not one thing in common between compartments')

        return common.pop()


class Day3(AdventOfCodePuzzle):

    def part_1(self, inputs: List[str]) -> int:
        backpacks = [Backpack(line) for line in inputs]
        return sum([b.common_priority for b in backpacks])

    def part_2(self, inputs: List[str]) -> int:
        backpacks = [Backpack(line) for line in inputs]
        common_priorities = []
        for group in grouper(backpacks, 3):
            common_item = Backpack.find_common_item_with_backpacks(group)
            common_priorities.append(Backpack.get_item_priority(common_item))

        return sum(common_priorities)
