from abc import ABC, abstractmethod
from typing import List


class AdventOfCodePuzzle(ABC):
    strip_input_lines = True

    @abstractmethod
    def part_1(self, inputs: List[str]):
        pass

    @abstractmethod
    def part_2(self, inputs: List[str]):
        pass
