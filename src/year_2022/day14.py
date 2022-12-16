from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class CaveWaterfall:
    class OffTheEdgeError(ValueError):
        pass

    class StoppedMovingError(ValueError):
        pass

    def __init__(self, inputs, add_floor=False) -> None:
        self.add_floor = add_floor
        rock_points = []
        for line in inputs:
            points = line.split(' -> ')
            for i in range(len(points) - 1):
                start_x, start_y = [int(val) for val in points[i].split(',')]
                end_x, end_y = [int(val) for val in points[i + 1].split(',')]

                self.add_rocks_between_points(rock_points, end_x, end_y, start_x, start_y)

        if add_floor:
            max_y = max([p[1] for p in rock_points])
            self.add_rocks_between_points(rock_points, 1000, max_y + 2, 0, max_y + 2)

        drop_point = (500, 0)
        min_x = min([p[0] for p in rock_points + [drop_point]])
        min_y = min([p[1] for p in rock_points + [drop_point]])

        norm_rock_points = [(x - min_x, y - min_y) for x, y in rock_points]
        norm_drop_point = (drop_point[0] - min_x, drop_point[1] - min_y)
        min_x = min([p[0] for p in norm_rock_points + [norm_drop_point]])
        min_y = min([p[1] for p in norm_rock_points + [norm_drop_point]])
        max_x = max([p[0] for p in norm_rock_points + [norm_drop_point]])
        max_y = max([p[1] for p in norm_rock_points + [norm_drop_point]])

        self.grid = np.zeros((max_y - min_y + 3, max_x - min_x + 3), dtype='U1')

        for r_x, r_y in norm_rock_points:
            self.grid[r_y, r_x] = '🪨'
        self.drop_x = norm_drop_point[0]
        self.drop_y = norm_drop_point[1]

        self.max_y, self.max_x = self.grid.shape
        self.max_x -= 1
        self.max_y -= 1

    def add_rocks_between_points(self, rock_points, end_x, end_y, start_x, start_y):
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                rock_points.append((x, y))

    def drop_sand(self):
        sand_x = self.drop_x
        sand_y = self.drop_y

        find_spot_for_sand = False
        while True:
            try:
                sand_x, sand_y = self.check_for_open(sand_x, sand_y)
                find_spot_for_sand = True
            except self.StoppedMovingError:
                break
            except self.OffTheEdgeError:
                find_spot_for_sand = False
                break
        if find_spot_for_sand:
            self.grid[sand_y, sand_x] = '🎾'
        return find_spot_for_sand

    def check_for_open(self, sand_x, sand_y):
        points_to_check = (
            (sand_x, sand_y + 1),
            (sand_x - 1, sand_y + 1),
            (sand_x + 1, sand_y + 1),
        )
        for x, y in points_to_check:
            if not (0 <= x <= self.max_x) or not (0 <= y <= self.max_y):
                raise self.OffTheEdgeError()
            elif self.grid[y, x] == '':
                return x, y
        raise self.StoppedMovingError()

    @property
    def sand_count(self):
        return (self.grid == '🎾').sum()

    def drop_all_the_sand(self):
        while True:
            if not self.drop_sand():
                break

        # Applying correction since loop above requires sand to at least make it one movemen from drop point
        # If we are using floor, we're filling it up to and including the drop point so we add it in manually
        if self.add_floor:
            self.grid[self.drop_y, self.drop_x] = '🎾'


class Day14(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        waterfall = CaveWaterfall(inputs)
        waterfall.drop_all_the_sand()
        return waterfall.sand_count

    def part_2(self, inputs: List[str]):
        waterfall = CaveWaterfall(inputs, add_floor=True)
        waterfall.drop_all_the_sand()
        return waterfall.sand_count
