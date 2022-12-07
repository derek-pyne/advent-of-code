import statistics
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class LineChecker:
    def __init__(self, line):
        self.line = line
        self.valid = False
        self.corrupt_score = 0
        self.incomplete = False
        self.open_characters = None
        self._check_validity()

    def _check_validity(self):
        open_to_close = dict({
            '(': ')',
            '[': ']',
            '{': '}',
            '<': '>',
        })

        open_characters = []
        for c in self.line:
            # Adding to open characters
            if c in open_to_close.keys():
                open_characters.append(c)
            else:
                # Trying to close but nothing to even attempt to close
                if len(open_characters) == 0:
                    self.corrupt_score = self._get_corrupt_point_value(c)
                    return

                # Removing open character and checking that it matches closing characer
                current_open = open_characters.pop()
                if open_to_close[current_open] != c:
                    self.corrupt_score = self._get_corrupt_point_value(c)
                    return
        self.corrupt_score = 0

        if len(open_characters) != 0:
            self.incomplete = True
            self.open_characters = open_characters
        self.valid = True

    def _get_corrupt_point_value(self, c) -> int:
        return {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137,
        }.get(c, 0)

    @property
    def autocomplete_score(self) -> int:
        if not self.incomplete:
            return 0

        autocomplete_points = {
            '(': 1,
            '[': 2,
            '{': 3,
            '<': 4
        }

        score = 0
        for c in self.open_characters[::-1]:
            score *= 5
            score += autocomplete_points[c]
        return score


class Day10(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        return sum([LineChecker(line).corrupt_score for line in inputs])

    def part_2(self, inputs: List[str]):
        autocomplete_scores = []
        for line in inputs:
            lc = LineChecker(line)
            if lc.incomplete:
                autocomplete_scores.append(lc.autocomplete_score)
        return statistics.median(autocomplete_scores)
