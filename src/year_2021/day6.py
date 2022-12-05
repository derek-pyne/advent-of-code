from collections import Counter
from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


# basically dies at 170
# def spawn(fish: List[int]) -> List[int]:
#     newbies = []
#     currents = []
#     for i, f in enumerate(fish):
#         if f == 0:
#             fish[i] = 6
#             newbies.append(8)
#         else:
#             fish[i] = f - 1
#     return fish + newbies

# def spawn(fish):
#     spawning_fish = fish == 0
#     fish[spawning_fish] = 6
#     fish[~spawning_fish] = fish[~spawning_fish] - 1
#     return np.concatenate((fish, np.ones(spawning_fish.sum())*8))


def spawn(fish_count):
    new_fish_count = {}

    # Number of new fish to spawn
    newbies = fish_count[0]

    # Decrementing normal fish
    for i in range(0, 8):
        new_fish_count[i] = fish_count[i + 1]

    new_fish_count[6] = new_fish_count[6] + newbies
    new_fish_count[8] = newbies
    return new_fish_count


def run_sim(fish_count, days):
    for i in range(days):
        fish_count = spawn(fish_count)
    return sum([c for c in fish_count.values()])


class Day6(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        fish_count = Counter([int(f) for f in inputs[0].split(',')])
        return run_sim(fish_count, 80)

    def part_2(self, inputs: List[str]) -> int:
        fish_count = Counter([int(f) for f in inputs[0].split(',')])
        return run_sim(fish_count, 256)
