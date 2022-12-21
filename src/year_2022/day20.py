from dataclasses import dataclass
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class MixingNum:
    value: int
    next: 'MixingNum' = None
    previous: 'MixingNum' = None

    def __repr__(self) -> str:
        return f'MixinNum(value={self.value}, next_value={self.next.value}, prev_value={self.previous.value})'


class MixingEncrypter:
    def __init__(self, inputs, multiplier=1):
        self.mixin_nums = [MixingNum(value=int(line) * multiplier) for i, line in enumerate(inputs)]

        for i, mn in enumerate(self.mixin_nums):
            mn.previous = self.mixin_nums[i - 1]
            mn.next = self.mixin_nums[(i + 1) % len(self.mixin_nums)]

    def traverse(self, starting_point=None):
        if starting_point is None:
            starting_point = self.mixin_nums[0]
        node = starting_point
        while node is not None and (node.next != starting_point):
            yield node
            node = node.next
        yield node

    def print_values(self, starting_point=None):
        nodes = []
        for node in self.traverse(starting_point):
            nodes.append(str(node.value))
        print(" -> ".join(nodes))

    def move_in_circle(self, node: MixingNum, n):
        forward = n >= 0
        iterations = abs(n) % (len(self.mixin_nums) - 1)
        for _ in range(iterations):
            if forward:
                prev_node = node.previous
                next_node = node.next

                # Removing current node
                prev_node.next = next_node
                next_node.previous = prev_node

                # Placing node in front of next node
                node.previous = next_node
                node.next = next_node.next
                next_node.next.previous = node
                next_node.next = node
            else:
                prev_node = node.previous
                next_node = node.next

                # Removing current node
                prev_node.next = next_node
                next_node.previous = prev_node

                # Placing node behind previous node
                node.next = prev_node
                node.previous = prev_node.previous
                prev_node.previous.next = node
                prev_node.previous = node

    def mix(self):
        for mn in self.mixin_nums:
            self.move_in_circle(mn, mn.value)

    def value_after_zero(self, n) -> MixingNum:
        zero_node = None
        for node in self.mixin_nums:
            if node.value == 0:
                zero_node = node
                break

        node = zero_node
        for _ in range(n % len(self.mixin_nums)):
            node = node.next
        return node

    def sum_values_after_zero(self, ns):
        nodes = [self.value_after_zero(n) for n in ns]
        return sum([node.value for node in nodes])


class Day20(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        encrypter = MixingEncrypter(inputs=inputs)
        encrypter.mix()
        return encrypter.sum_values_after_zero(ns=[1000, 2000, 3000])

    def part_2(self, inputs: List[str]):
        encrypter = MixingEncrypter(inputs=inputs, multiplier=811589153)
        for _ in range(10):
            encrypter.mix()
        return encrypter.sum_values_after_zero(ns=[1000, 2000, 3000])
