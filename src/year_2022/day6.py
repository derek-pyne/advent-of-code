from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


def first_marker(data, marker_size) -> int:
    for i in range(len(data) - marker_size - 1):
        if len(set(data[i:i + marker_size])) == marker_size:
            return i + marker_size
    return -1


class Day6(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        return first_marker(inputs[0], 4)

    def part_2(self, inputs: List[str]):
        return first_marker(inputs[0], 14)
