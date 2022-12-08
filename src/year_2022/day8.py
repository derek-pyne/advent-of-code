from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Day8(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        trees = np.array([[int(x) for x in line] for line in inputs])
        visible = self.forest_views(trees)
        return int(visible.sum())

    def part_2(self, inputs: List[str]):
        trees = np.array([[int(x) for x in line] for line in inputs])
        scenic_scores = self.scenic_score(trees)
        return int(scenic_scores.max())

    @staticmethod
    def forest_views(trees):
        y_lim, x_lim = trees.shape
        visible = np.zeros(trees.shape)
        for x in range(0, x_lim):
            for y in range(0, y_lim):
                left = not (trees[y, :x] >= trees[y, x]).any()
                right = not (trees[y, x + 1:] >= trees[y, x]).any()
                up = not (trees[:y, x] >= trees[y, x]).any()
                down = not (trees[y + 1:, x] >= trees[y, x]).any()
                if left or right or up or down:
                    visible[y, x] = True
        return visible

    @staticmethod
    def scenic_score(trees):
        y_lim, x_lim = trees.shape
        scenic_scores = np.zeros(trees.shape)
        for x in range(0, x_lim):
            for y in range(0, y_lim):
                # Gathering views in each direction, going out from current tree
                views = dict(
                    left=trees[y, :x][::-1],
                    right=trees[y, x + 1:],
                    up=trees[:y, x][::-1],
                    down=trees[y + 1:, x],
                )

                # Building scores in each direction.
                score = 1
                for direction, t in views.items():
                    direction_score = 0
                    # Iterating and adding to score in this direction until we hit a big tree
                    for i in t:
                        direction_score += 1
                        if i >= trees[y, x]:
                            break
                    score *= direction_score

                scenic_scores[y, x] = score
        return scenic_scores
