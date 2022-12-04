from operator import attrgetter
from typing import List

import pandas as pd

from src.advent_of_code_puzzle import AdventOfCodePuzzle
from src.utils import grouper


class BingoBoard:

    def __init__(self, raw_board_list_strings) -> None:
        self.board = pd.DataFrame([[int(s) for s in board_line.split()] for board_line in raw_board_list_strings[:5]])
        self.nums_selected = pd.DataFrame(data=False, index=self.board.index, columns=self.board.columns)
        self.nums_drawn = 0
        self.final_num = 0
        self.score = 0

    def draw_number(self, num: int):
        # Already won, don't need to draw again
        if self.score != 0:
            return

        self.nums_drawn += 1
        self.final_num = num
        self.nums_selected = self.nums_selected | (self.board == num)
        if self.check_if_winner():
            self.score = int(self.board[~self.nums_selected].sum().sum() * num)
        else:
            return

    def check_if_winner(self) -> bool:
        if (self.nums_selected.sum(axis=1) == 5).any():
            return True
        elif (self.nums_selected.sum(axis=0) == 5).any():
            return True
        else:
            return False


def run_boards(inputs: List[str]) -> List[BingoBoard]:
    drawn_numbers = [int(s) for s in inputs[0].split(',')]
    boards = []
    for board_list in grouper(inputs[2:], 6):
        boards.append(BingoBoard(board_list))
    for num in drawn_numbers:
        for board in boards:
            board.draw_number(num=num)
    return boards


class Day4(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        boards = run_boards(inputs)
        return min(boards, key=attrgetter('nums_drawn')).score

    def part_2(self, inputs: List[str]) -> int:
        boards = run_boards(inputs)
        return max(boards, key=attrgetter('nums_drawn')).score
