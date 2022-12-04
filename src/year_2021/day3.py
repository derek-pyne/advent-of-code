from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class PowerConsumer:

    def __init__(self, readings: List[str]) -> None:
        self.readings = readings
        self.line_len = len(self.readings[0])
        self.compute_power()
        self.reading_eliminator(most_common=False)
        self.life_support = self.reading_eliminator(most_common=True) * self.reading_eliminator(most_common=False)

    def compute_counts(self, readings):
        counts = []
        for reading in readings:
            for i, bit in enumerate(reading):
                if i >= len(counts):
                    counts.append({})

                if bit not in counts[i]:
                    counts[i][bit] = 0

                counts[i][bit] += 1
        return counts

    def compute_power(self):
        counts = self.compute_counts(self.readings)

        epsilon = ''
        gamma = ''
        for position in counts:
            if position['1'] < position['0']:
                epsilon += '1'
                gamma += '0'
            else:
                gamma += '1'
                epsilon += '0'

        self.epsilon_val = int(epsilon, 2)
        self.gamma_val = int(gamma, 2)
        self.power_consumption = self.epsilon_val * self.gamma_val

    def reading_eliminator(self, most_common=True):

        possible_values = self.readings.copy()
        counts = self.compute_counts(self.readings)
        for i in range(self.line_len):
            if most_common:
                target = '1' if counts[i]['1'] >= counts[i]['0'] else '0'
            else:
                # least_common
                target = '0' if counts[i]['0'] <= counts[i]['1'] else '1'
            new_possible_values = []
            for value in possible_values:
                if value[i] == target:
                    new_possible_values.append(value)

            if len(new_possible_values) == 1:
                return int(new_possible_values[0], 2)
            else:
                possible_values = new_possible_values
                counts = self.compute_counts(possible_values)
        raise ValueError('Never narrowed down to a single value')


class Day3(AdventOfCodePuzzle):

    def part_1(self, inputs: List[str]) -> int:
        return PowerConsumer(readings=inputs).power_consumption

    def part_2(self, inputs: List[str]) -> int:
        return PowerConsumer(readings=inputs).life_support
