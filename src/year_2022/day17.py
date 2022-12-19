from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


# Needed tons of help from: https://github.com/ephemient/aoc2022/blob/main/py/aoc2022/day17.py
# for part 2
class Tetris:
    pieces = [
        np.array([[True, True, True, True]]),
        np.array([[False, True, False], [True, True, True], [False, True, False]]),
        np.array([[True, True, True], [False, False, True], [False, False, True]]),
        np.array([[True], [True], [True], [True]]),
        np.array([[True, True], [True, True]]),
    ]

    def __init__(self, jets) -> None:
        self.grid = np.zeros((5000000, 7), dtype=bool)
        self.pieces_dropped = 0
        self.jets = jets
        self.jet_move_count = 0
        self.top_rock = 0
        self.cycle_fast_forward_height = 0
        self.y_offset = 0
        self.hashes = {}

    def get_new_piece(self):
        new_piece = self.pieces[self.piece_index]
        self.pieces_dropped += 1
        return new_piece

    @property
    def piece_index(self):
        return self.pieces_dropped % len(self.pieces)

    def move_x_from_jets(self, x, y, new_piece) -> int:
        direction = self.jets[self.jet_index]
        self.jet_move_count += 1
        if direction == '<':
            new_x = x - 1
        elif direction == '>':
            new_x = x + 1
        else:
            raise ValueError(f'Bad direction: {direction}')

        if self.check_if_fits(new_x, y, new_piece):
            return new_x
        else:
            return x

    @property
    def jet_index(self):
        return self.jet_move_count % len(self.jets)

    def check_if_fits(self, x, y, new_piece) -> bool:
        height, width = new_piece.shape
        grid_placement_shape = self.grid[y:y + height, x:x + width].shape
        if grid_placement_shape != new_piece.shape:
            return False
        grid_piece_overlap = self.grid[y:y + height, x:x + width] & new_piece
        return grid_piece_overlap.sum() == 0

    def drop_pieces(self, n):
        while True:
            new_piece = self.get_new_piece()
            height, width = new_piece.shape
            y = self.top_rock + 3
            x = 2
            while True:
                x = self.move_x_from_jets(x, y, new_piece)

                new_y = y - 1
                if self.check_if_fits(x, new_y, new_piece):
                    y = new_y
                else:
                    self.check_if_fits(x, new_y, new_piece)
                    self.grid[y:y + height, x:x + width] = new_piece | self.grid[y:y + height, x:x + width]
                    if y + height > self.top_rock:
                        self.top_rock = y + height
                    break

            # Checking for two rows that block all pieces below
            # We basically keep resetting the grid every time we detect a blocking section like this
            if (self.grid[y, :] | self.grid[y - 1, :]).sum() == 7:
                self.top_rock -= (y - 1)
                self.grid = self.grid[y - 1:]
                self.y_offset += (y - 1)

            # Because we keep resetting the grid, now we can work our way up from this 'fresh' start and hash
            # the state as we go. Then, once we reset again, if we start to match any of these hashs from the previous
            # reset run, then we know we have detected a cycle
            hsh = f'{hash(np.array2string(self.grid[0:self.top_rock + 1]))}|{self.piece_index}|{self.jet_index}'
            if hsh in self.hashes:
                prev_blocks, prev_height = self.hashes[hsh]
                cycle_len = self.pieces_dropped - prev_blocks
                if cycle_len < (n - self.pieces_dropped):
                    cycle_height = self.total_height - prev_height
                    # skip time ahead when we detect a cycle!
                    ncycles = (n - self.pieces_dropped) // cycle_len
                    print(
                        f'Skipping ahead from {self.pieces_dropped}: {ncycles} cycles of length {cycle_len} with height {cycle_height}')
                    self.pieces_dropped += ncycles * cycle_len
                    self.y_offset += ncycles * cycle_height
            else:
                self.hashes[hsh] = (self.pieces_dropped, self.total_height)

            if self.pieces_dropped == n:
                break

    def print(self):
        lines_to_print = ['+-------+']
        for row in self.grid[:self.top_rock + 3, :]:
            lines_to_print.append(f'|{"".join(["#" if val else "." for val in row])}|')

        print()
        for line in lines_to_print[::-1]:
            print(line)

    @property
    def total_height(self):
        return self.top_rock + self.y_offset


class Day17(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        t = Tetris(jets=inputs[0])
        t.drop_pieces(n=2022)
        return t.total_height

    def part_2(self, inputs: List[str]):
        t = Tetris(jets=inputs[0])
        t.drop_pieces(n=1000000000000)
        return t.total_height
