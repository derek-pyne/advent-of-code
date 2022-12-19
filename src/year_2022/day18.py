from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class VolcanoBlob:

    def __init__(self, inputs) -> None:
        self.points = []
        for p in inputs:
            x, y, z = p.split(',')
            self.points.append(
                (int(x), int(y), int(z))
            )

        max_x = max([p[0] for p in self.points])
        max_y = max([p[1] for p in self.points])
        max_z = max([p[2] for p in self.points])

        self.blob = np.zeros((max_z + 2, max_y + 2, max_x + 2), dtype='U1')
        self.blob.fill('.')
        self.blob = np.pad(self.blob, 1, constant_values='o')
        self.z_lim, self.y_lim, self.x_lim = self.blob.shape
        self.x_lim -= 1
        self.y_lim -= 1
        self.z_lim -= 1

        for x, y, z in self.points:
            self.blob[z, y, x] = '#'

    def side_count(self):
        side_count = 0
        for x, y, z in self.points:
            if self.blob[z, y, x - 1] != '#':
                side_count += 1
            if self.blob[z, y - 1, x] != '#':
                side_count += 1
            if self.blob[z - 1, y, x] != '#':
                side_count += 1
            if self.blob[z, y, x + 1] != '#':
                side_count += 1
            if self.blob[z, y + 1, x] != '#':
                side_count += 1
            if self.blob[z + 1, y, x] != '#':
                side_count += 1
        return side_count

    def fill_air(self):
        while True:
            # Iterating until we aren't adding any more air
            # Could do something clever where we go from the outside and spiral in
            # But easier to just keep repeatedly scanning until we stop adding air
            air_added = False
            for z in range(self.z_lim):
                for y in range(self.y_lim):
                    for x in range(self.x_lim):
                        # Checking if we are at an inner point
                        if self.blob[z, y, x] != '.':
                            continue

                        # Checking if this point is touching air
                        # If so, then it should also be air
                        if self.is_point_touching_air(x, y, z):
                            self.blob[z, y, x] = 'o'
                            air_added = True

            if not air_added:
                break

    def side_count_touching_air(self):
        side_count = 0
        for z in range(self.z_lim):
            for y in range(self.y_lim):
                for x in range(self.x_lim):
                    # Checking that we are on rock and that this rock is touching air
                    if not (self.blob[z, y, x] == '#' and self.is_point_touching_air(x, y, z)):
                        continue

                    # This is now an outer rock, lets count the sides that are touching air
                    if self.blob[z, y, x - 1] == 'o':
                        side_count += 1
                    if self.blob[z, y - 1, x] == 'o':
                        side_count += 1
                    if self.blob[z - 1, y, x] == 'o':
                        side_count += 1
                    if self.blob[z, y, x + 1] == 'o':
                        side_count += 1
                    if self.blob[z, y + 1, x] == 'o':
                        side_count += 1
                    if self.blob[z + 1, y, x] == 'o':
                        side_count += 1
        return side_count

    def is_point_touching_air(self, x, y, z):
        points_to_check = [
            [z, y, x - 1],
            [z, y - 1, x],
            [z - 1, y, x],
            [z, y, x + 1],
            [z, y + 1, x],
            [z + 1, y, x],
        ]
        for p_z, p_y, p_x in points_to_check:
            if 0 <= p_x <= self.x_lim and 0 <= p_y <= self.y_lim and 0 <= p_z <= self.z_lim \
                    and self.blob[p_z, p_y, p_x] == 'o':
                return True
        return False


class Day18(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        vb = VolcanoBlob(inputs)
        return vb.side_count()

    def part_2(self, inputs: List[str]):
        vb = VolcanoBlob(inputs)
        vb.fill_air()
        return vb.side_count_touching_air()
