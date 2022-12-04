import re
from dataclasses import dataclass
from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class Vent:
    start_x: int
    start_y: int
    end_x: int
    end_y: int

    def biggest_x(self):
        return max([self.start_x, self.end_x])

    def biggest_y(self):
        return max([self.start_y, self.end_y])

    @property
    def is_horizontal_or_vertical(self) -> bool:
        return (self.start_x == self.end_x) or (self.start_y == self.end_y)

    @property
    def min_x(self):
        return min([self.start_x, self.end_x])

    @property
    def max_x(self):
        return max([self.start_x, self.end_x])

    @property
    def min_y(self):
        return min([self.start_y, self.end_y])

    @property
    def max_y(self):
        return max([self.start_y, self.end_y])


def parse_vents(inputs: List[str]) -> List[Vent]:
    vents = []
    for line in inputs:
        match = re.match('(\d*),(\d*) -> (\d*),(\d*)', line)
        if not match:
            raise ValueError(f'Failed to parse: {line}')
        vents.append(Vent(
            start_x=int(match.groups()[0]),
            start_y=int(match.groups()[1]),
            end_x=int(match.groups()[2]),
            end_y=int(match.groups()[3]),
        ))
    return vents


def vent_grid_hotspots(inputs, hor_or_vert_only=True):
    vents = parse_vents(inputs)
    grid_shape = (max([v.biggest_x() for v in vents]) + 1, max([v.biggest_y() for v in vents]) + 1)

    grid = np.zeros(grid_shape)
    for vent in vents:
        if hor_or_vert_only and not vent.is_horizontal_or_vertical:
            continue
        v_grid = np.zeros(grid_shape)

        if vent.is_horizontal_or_vertical:
            v_grid[vent.min_y:(vent.max_y + 1), vent.min_x:(vent.max_x + 1)] = 1
        else:
            # 45 degree line
            x_adjustment = 1 if vent.end_x >= vent.start_x else -1
            y_adjustment = 1 if vent.end_y >= vent.start_y else -1
            x_vals = list(range(vent.start_x, vent.end_x + x_adjustment, x_adjustment))
            y_vals = list(range(vent.start_y, vent.end_y + y_adjustment, y_adjustment))

            for x, y in zip(x_vals, y_vals):
                v_grid[y, x] = 1
        grid += v_grid
    return (grid >= 2).sum()


class Day5(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        return vent_grid_hotspots(inputs)

    def part_2(self, inputs: List[str]) -> int:
        return vent_grid_hotspots(inputs, hor_or_vert_only=False)
