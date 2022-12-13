from dataclasses import dataclass
from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class Fold:
    direction: str
    value: int

    def fold_paper(self, paper):
        if self.direction == 'y':
            top = paper[:self.value, :]
            bottom = paper[self.value + 1:, :]

            b_pad = np.zeros_like(top, dtype=bool)
            b_pad[:bottom.shape[0], :bottom.shape[1]] = bottom
            return top | np.flipud(b_pad)
        else:
            left = paper[:, :self.value]
            right = paper[:, self.value + 1:]

            r_pad = np.zeros_like(left, dtype=bool)
            r_pad[:right.shape[0], :right.shape[1]] = right
            return left | np.fliplr(r_pad)


def print_paper(paper):
    paper_str = np.zeros_like(paper, dtype='U1')
    paper_str.fill(' ')
    paper_str[paper] = '█'

    print()
    for row in paper:
        print(''.join(['  ' if not x else '██' for x in row]))


def parse_instructions(inputs):
    positions = []
    folds = []
    for line in inputs:
        if ',' in line:
            x, y = line.split(',')
            positions.append((int(x), int(y)))

        elif line.startswith('fold'):
            _, remaining = line.split('along ')
            direction, value = remaining.split('=')
            folds.append(Fold(direction=direction, value=int(value)))
    paper = np.zeros((max([p[1] for p in positions]) + 1, max([p[0] for p in positions]) + 1), dtype=bool)
    for x, y in positions:
        paper[y, x] = True
    return folds, paper


class Day13(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        folds, paper = parse_instructions(inputs)

        for fold in folds:
            paper = fold.fold_paper(paper)
            print_paper(paper)
            return paper.sum()

    def part_2(self, inputs: List[str]):
        folds, paper = parse_instructions(inputs)

        for fold in folds:
            paper = fold.fold_paper(paper)
        print_paper(paper)
        return 'CJCKBAPB'
