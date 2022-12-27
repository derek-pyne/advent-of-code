from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class SNAFUConverter:
    snafu_map = {
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2': 2
    }

    @staticmethod
    def to_decimal(snafu):
        num = 0
        for power, c in enumerate(snafu[::-1]):
            num += SNAFUConverter.snafu_map[c] * 5 ** power
        return num

    def to_snafu(self, decimal):
        pass


def add(num1, num2):
    convert = {
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2': 2,
        -2:  '=',
        -1:  '-',
        0:   '0',
        1:   '1',
        2:   '2',
    }
    extra = 0
    result = ''

    max_len = max(len(num2), len(num1))
    for d1, d2 in zip(num1.rjust(max_len, '0')[::-1], num2.rjust(max_len, '0')[::-1]):
        digit_sum = convert[d1] + convert[d2] + extra
        if digit_sum > 2:
            extra = 1
            result += convert[digit_sum - 5]
        elif digit_sum < -2:
            extra = -1
            result += convert[digit_sum + 5]
        else:
            extra = 0
            result += convert[digit_sum]

    result += convert[extra]
    return result[::-1]


class Day25(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        nums = [SNAFUConverter.to_decimal(snafu_num) for snafu_num in inputs]
        num_sum = sum(nums)

        # Can add directly, don't need to convert back and forth
        snafu_sum = '0'
        for snafu_num in inputs:
            snafu_sum = add(snafu_sum, snafu_num)
        return snafu_sum.lstrip('0')

    def part_2(self, inputs: List[str]):
        return 1
