from collections import Counter
from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Day9(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        ocean_floor = np.array([[int(x) for x in line] for line in inputs])
        minima_risk = self.find_minimas(ocean_floor)

        return int(minima_risk.sum())

    def part_2(self, inputs: List[str]):
        ocean_floor = np.array([[int(x) for x in line] for line in inputs])
        minima_risk = self.find_minimas(ocean_floor)
        minimas = minima_risk > 0
        basins = self.find_basins(ocean_floor, minimas)

        counts = Counter([x for line in basins.tolist() for x in line])
        if -1 in counts:
            counts.pop(-1)

        return np.prod([x[1] for x in counts.most_common(3)])

    def find_minimas(self, ocean_floor):
        minima_risk = np.zeros(shape=ocean_floor.shape)
        y_lim, x_lim = ocean_floor.shape
        for x in range(0, x_lim):
            for y in range(0, y_lim):
                neighbors = []
                if x - 1 >= 0:
                    neighbors.append(ocean_floor[y, x - 1])
                if x + 1 < x_lim:
                    neighbors.append(ocean_floor[y, x + 1])

                if y - 1 >= 0:
                    neighbors.append(ocean_floor[y - 1, x])
                if y + 1 < y_lim:
                    neighbors.append(ocean_floor[y + 1, x])

                if ocean_floor[y, x] < min(neighbors):
                    minima_risk[y, x] = 1 + ocean_floor[y, x]
        return minima_risk

    def find_basins(self, ocean_floor, minimas):
        basins = np.zeros(shape=ocean_floor.shape)

        # 9 is the ceiling, making this a special number so its like a wall
        basins[ocean_floor == 9] = -1

        # Numbering basins
        y_lim, x_lim = ocean_floor.shape
        basin_i = 1
        for x in range(0, x_lim):
            for y in range(0, y_lim):
                if minimas[y, x]:
                    basins[y, x] = basin_i
                    basin_i += 1

        while True:
            change_made = False
            for x in range(0, x_lim):
                for y in range(0, y_lim):
                    # Continuing if we are looking at either a wall, or an unassigned section
                    if basins[y, x] == -1 or basins[y, x] == 0:
                        continue

                    # We must be at an existing basin square. 
                    # We can assign the zeroes around it to this basins number
                    basin_i = basins[y, x]
                    if x - 1 >= 0 and basins[y, x - 1] == 0:
                        basins[y, x - 1] = basin_i
                        change_made = True
                    if x + 1 < x_lim and basins[y, x + 1] == 0:
                        basins[y, x + 1] = basin_i
                        change_made = True
                    if y - 1 >= 0 and basins[y - 1, x] == 0:
                        basins[y - 1, x] = basin_i
                        change_made = True
                    if y + 1 < y_lim and basins[y + 1, x] == 0:
                        basins[y + 1, x] = basin_i
                        change_made = True

            if not change_made:
                break

        return basins
