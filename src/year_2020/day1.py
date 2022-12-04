from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


def get_sum_nums(nums, target):
    for num in nums:
        desired = target - num
        if desired in nums:
            return num, desired

    return None, None


def get_sum_nums(nums, target):
    for num in nums:
        desired = target - num
        if desired in nums:
            return num, desired

    return None, None


class Day1(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        nums = [int(input) for input in inputs]

        num, desired = get_sum_nums(nums, target=2020)
        return num * desired

    def part_2(self, inputs: List[str]) -> int:
        nums = [int(input) for input in inputs]
        for num in nums:
            other_nums = nums.copy()
            other_nums.remove(num)
            num2, num3 = get_sum_nums(other_nums, target=2020 - num)
            if num2 is not None:
                return num * num2 * num3
