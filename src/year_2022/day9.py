from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Knot:

    def __init__(self) -> None:
        self.tail_x = 500
        self.tail_y = 500
        self.head_x = 500
        self.head_y = 500
        self.head_visited = np.zeros([1000, 1000])
        self.head_visited[self.head_y, self.head_x] = 1
        self.tail_visited = np.zeros_like(self.head_visited)
        self.tail_visited[self.tail_y, self.tail_x] = 1

    def display_current_position(self):
        grid = np.zeros_like(self.head_visited, 'U1')
        grid.fill('.')
        grid[self.tail_y, self.tail_x] = 'T'
        grid[self.head_y, self.head_x] = 'H'
        print(np.flipud(grid))

    def move(self, direction: str, amount: int):
        for _ in range(amount):
            self.move_step(direction=direction)

    def move_step(self, direction: str):
        self.move_head_in_direction(direction)
        self.adjust_tail_to_follow_head()

    def move_head_in_direction(self, direction):
        if direction == 'U':
            self.set_head(self.head_x, self.head_y+1)
        elif direction == 'D':
            self.set_head(self.head_x, self.head_y-1)
        elif direction == 'R':
            self.set_head(self.head_x+1, self.head_y)
        elif direction == 'L':
            self.set_head(self.head_x-1, self.head_y)
        else:
            raise ValueError(f'Invalid direction: {direction}')

    def set_head(self, x, y):
        self.head_y = y
        self.head_x = x
        self.head_visited[y, x] = 1

    def adjust_tail_to_follow_head(self):
        # Returning if head and tail are currently touching
        if abs(self.head_x - self.tail_x) <= 1 and abs(self.head_y - self.tail_y) <= 1:
            return

        # If in the same row, only move if gap is bigger then two
        # Otherwise move diagonally in whatever direction there is any gap
        gap_check = 2 if self.head_y == self.tail_y or self.head_x == self.tail_x else 1

        if (self.head_x - self.tail_x) >= gap_check:
            # Head is running away to the right
            self.tail_x += 1
        elif (self.head_x - self.tail_x) <= -gap_check:
            # Head is running away to the left
            self.tail_x -= 1

        if (self.head_y - self.tail_y) >= gap_check:
            # Head is running away upwards
            self.tail_y += 1
        elif (self.head_y - self.tail_y) <= -gap_check:
            # Head is running away downwards
            self.tail_y -= 1

        self.tail_visited[self.tail_y, self.tail_x] = 1


class Rope:

    def __init__(self, knot_num=10) -> None:
        self.knots = [Knot() for _ in range(knot_num)]

    def move(self, direction: str, amount: int):
        for _ in range(amount):
            self.knots[0].move_step(direction=direction)
            previous_rope = self.knots[0]
            for i in range(1, 10):
                current_rope = self.knots[i]
                current_rope.set_head(x=previous_rope.tail_x, y=previous_rope.tail_y)
                current_rope.adjust_tail_to_follow_head()
                previous_rope = current_rope

    def display_current_position(self):
        grid = np.zeros_like(self.tail_visited, 'U1')
        grid.fill('.')
        for i, k in enumerate(self.knots):
            grid[k.head_y, k.head_x] = str(i) if i != 0 else 'H'
        print(np.flipud(grid))

    @property
    def tail_visited(self):
        # return self.knots[0].tail_visited + sum([k.tail_visited for k in self.knots[1:]])
        return self.knots[-1].head_visited


class Day9(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        k = Knot()
        print()
        k.display_current_position()
        for command in inputs:
            d, num = command.split()
            print(f'Command: {command}')
            k.move(d, int(num))
            k.display_current_position()
        return int(k.tail_visited.sum())

    def part_2(self, inputs: List[str]):
        rope = Rope()
        print()
        rope.display_current_position()
        for command in inputs:
            d, num = command.split()
            print(f'Command: {command}')
            rope.move(d, int(num))
            rope.display_current_position()
        return int(rope.tail_visited.sum())
