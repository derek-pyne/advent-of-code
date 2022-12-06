from typing import List
import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


def fuel_to_rearrange(positions, target) -> int:
    diffs = positions - target
    return np.abs(diffs).sum()


def fuel_to_rearrange2(positions, target) -> int:
    diffs = positions - target
    diffs = np.abs(diffs)

    costerfunc = np.vectorize(lambda x: x * (x + 1) // 2)
    diffs = costerfunc(diffs)

    return diffs.sum()


class Day7(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        positions = np.array([int(x) for x in inputs[0].split(',')])

        fuel_costs = []
        for i in range(positions.min(), positions.max() + 1):
            fuel_costs.append(fuel_to_rearrange(positions, i))
        return min(fuel_costs)

    def part_2(self, inputs: List[str]):
        positions = np.array([int(x) for x in inputs[0].split(',')])

        fuel_costs = []
        for i in range(positions.min(), positions.max() + 1):
            fuel_costs.append(fuel_to_rearrange2(positions, i))
        return min(fuel_costs)
