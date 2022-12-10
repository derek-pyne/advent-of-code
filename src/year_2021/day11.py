from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class OctopusField:

    def __init__(self, inputs) -> None:
        self.energy_grid = np.array([[int(x) for x in line] for line in inputs])
        self.y_lim, self.x_lim = self.energy_grid.shape
        self.total_flashes = 0

    def energy_step(self) -> bool:
        # Returns true if its a mega flash
        self.energy_grid += 1

        flashed = np.zeros_like(self.energy_grid, dtype=bool)
        while True:
            did_something_flash = False
            for iy, ix in np.ndindex(self.energy_grid.shape):
                if self.energy_grid[iy, ix] > 9 and not flashed[iy, ix]:
                    self.total_flashes += 1
                    did_something_flash = True
                    flashed[iy, ix] = True
                    self.energy_grid[
                    max(iy - 1, 0):min(iy + 2, self.y_lim),
                    max(ix - 1, 0):min(ix + 2, self.x_lim)
                    ] += 1
            if not did_something_flash:
                break
        self.energy_grid[self.energy_grid > 9] = 0
        return (flashed == False).sum() == 0


class Day11(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        of = OctopusField(inputs)
        for _ in range(100):
            of.energy_step()
        return of.total_flashes

    def part_2(self, inputs: List[str]):
        of = OctopusField(inputs)
        for i in range(10000):
            mega_flash = of.energy_step()
            if mega_flash:
                return i + 1
