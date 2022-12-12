import copy
from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class MountainPath:
    def __init__(self, heights, x, y) -> None:
        self.heights = heights
        self.path = np.zeros_like(self.heights, dtype='U1')
        self.path.fill('.')
        self.y_lim, self.x_lim = heights.shape
        self.position_x = x
        self.position_y = y
        self.path[self.position_y, self.position_x] = 'S'

    def set_position(self, x, y, character):
        if self.path[self.position_y, self.position_x] != 'S':
            self.path[self.position_y, self.position_x] = character
        if self.heights[y, x] == 'E':
            self.path[y, x] = 'E'
        self.position_x = x
        self.position_y = y

    @property
    def steps(self):
        return (self.path != '.').sum() - 1

    def is_step_valid(self, x, y):
        if x < 0 or x >= self.x_lim or y < 0 or y >= self.y_lim:
            return False

        if self.path[y, x] in ['S', 'E']:
            return True
        elif self.path[y, x] != '.':
            return False
        else:
            return self.is_downward_step(x, y)

    def is_downward_step(self, new_x, new_y):
        new_step = self.heights[new_y, new_x]
        current_step = self.heights[self.position_y, self.position_x]
        if current_step == 'S':
            return True

        if new_step == 'E':
            return current_step == 'z'

        return (ord(new_step) - ord(current_step)) <= 1

    def is_at_end(self):
        return self.heights[self.position_y, self.position_x] == 'E'

    def possible_next_steps(self) -> List['MountainPath']:
        possible_directions = [
            (self.position_x - 1, self.position_y, '<'),
            (self.position_x + 1, self.position_y, '>'),
            (self.position_x, self.position_y - 1, '^'),
            (self.position_x, self.position_y + 1, 'v'),
        ]

        paths_to_explore = []
        for x, y, character in possible_directions:
            if self.is_step_valid(x, y):
                new_path = copy.deepcopy(self)
                new_path.set_position(x, y, character)
                paths_to_explore.append(new_path)
        return paths_to_explore


def find_end(root) -> MountainPath:
    explored_positions = np.zeros_like(root.heights, dtype=bool)
    explored_positions[root.position_y, root.position_x] = True

    paths_to_explore = [root]
    while len(paths_to_explore) != 0:
        path = paths_to_explore.pop(0)
        if path.is_at_end():
            return path

        possible_next_steps = path.possible_next_steps()

        for possible_next_step in possible_next_steps:
            if not explored_positions[possible_next_step.position_y, possible_next_step.position_x]:
                explored_positions[possible_next_step.position_y, possible_next_step.position_x] = True
                paths_to_explore.append(possible_next_step)
    return None


class Day12(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        heights = np.array([[x for x in line] for line in inputs])
        result = np.where(heights == 'S')
        starting_points = list(zip(result[0], result[1]))

        min_paths = []
        for starting_point in starting_points:
            root = MountainPath(heights=heights, x=starting_point[1], y=starting_point[0])
            min_paths.append(find_end(root=root))

        min_path = min([p for p in min_paths if p is not None], key=lambda x: x.steps)
        print()
        print(min_path.path)
        return min_path.steps

    def part_2(self, inputs: List[str]):
        heights = np.array([[x for x in line] for line in inputs])
        result = np.where((heights == 'S') | (heights == 'a'))
        starting_points = list(zip(result[0], result[1]))

        min_paths = []
        for starting_point in starting_points:
            root = MountainPath(heights=heights, x=starting_point[1], y=starting_point[0])
            min_paths.append(find_end(root=root))

        min_path = min([p for p in min_paths if p is not None], key=lambda x: x.steps)
        print()
        print(min_path.path)
        return min_path.steps
