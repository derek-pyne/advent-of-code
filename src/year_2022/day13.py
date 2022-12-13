import json
from dataclasses import dataclass
from functools import total_ordering
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle
from src.utils import grouper


@dataclass
@total_ordering
class Packet:
    data: List

    def __eq__(self, other: 'Packet') -> bool:
        return self.data == other.data

    def __lt__(self, other) -> bool:
        order = self.check_order(self.data, other.data)
        if order is not None:
            return order
        else:
            return False

    @staticmethod
    def check_order(left, right) -> bool:
        left_reduce = left.copy()
        right_reduce = right.copy()

        while True:
            if len(left_reduce) == 0 and len(right_reduce) == 0:
                return None
            elif len(left_reduce) == 0:
                return True
            elif len(right_reduce) == 0:
                return False

            left_val = left_reduce.pop(0)
            right_val = right_reduce.pop(0)

            if type(left_val) == list and type(right_val) == int:
                right_val = [right_val]
            elif type(left_val) == int and type(right_val) == list:
                left_val = [left_val]

            if type(left_val) == int and type(right_val == int):
                if left_val != right_val:
                    return left_val < right_val
            elif type(left_val) == list and type(right_val == list):
                result = Packet.check_order(left_val, right_val)
                if result is not None:
                    return result


class Day13(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        correct_pairs = []
        for i, (left, right, _) in enumerate(grouper(inputs, n=3)):
            if Packet(data=json.loads(left)) < Packet(data=json.loads(right)):
                correct_pairs.append(i+1)
        return sum(correct_pairs)

    def part_2(self, inputs: List[str]):
        div_1 = Packet(data=[[2]])
        div_2 = Packet(data=[[6]])
        packets = [
            div_1,
            div_2,
        ]
        for line in inputs:
            if len(line) != 0:
                packets.append(Packet(data=json.loads(line)))
        packets.sort()
        return (packets.index(div_1) + 1) * (packets.index(div_2) + 1)
