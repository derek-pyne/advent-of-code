from itertools import zip_longest
from operator import attrgetter

import pandas as pd

f_path = '2021/inputs/day4.txt'


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


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


with open(f_path) as f:
    drawn_numbers = [int(s) for s in f.readline().strip().split(',')]
    f.readline()
    board_input = [line.strip() for line in f]
    boards = []
    for board_list in grouper(board_input, 6):
        boards.append(BingoBoard(board_list))

for num in drawn_numbers:
    for board in boards:
        board.draw_number(num=num)

first_winner = min(boards, key=attrgetter('nums_drawn'))
print(f'First winner score: {first_winner.score}')

last_winner = max(boards, key=attrgetter('nums_drawn'))
print(f'Last winner score: {last_winner.score}')
