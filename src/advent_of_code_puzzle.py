from abc import ABC, abstractmethod
from typing import List


class AdventOfCodePuzzle(ABC):

    @abstractmethod
    def part_1(self, inputs: List[str]) -> int:
        pass

    @abstractmethod
    def part_2(self, inputs: List[str]) -> int:
        pass
