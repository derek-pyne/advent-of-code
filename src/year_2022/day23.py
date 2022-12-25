from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class ElfGarden:

    def __init__(self, inputs) -> None:
        self.garden = np.array([[1 if x == '#' else 0 for x in line] for line in inputs])
        self.garden = np.pad(self.garden, self.garden.shape[0] * 2, constant_values=0)
        # self.garden = np.pad(self.garden, 1, constant_values=0)
        self.new_garden = np.zeros_like(self.garden)
        self.proposed_moves = np.zeros_like(self.garden)

    def propose_and_move(self, n, print_garden=False):
        for i in range(n):
            # Filling proposals
            self.proposed_moves = np.zeros_like(self.garden)
            for index, p in np.ndenumerate(self.garden):
                if p == 1:
                    self.single_elf_propose(index, direction_idx=i % 4)

            self.new_garden = np.zeros_like(self.garden)
            # Actually making moves now
            for index, p in np.ndenumerate(self.garden):
                if p == 1:
                    self.single_elf_move(index, direction_idx=i % 4)

            # No movement
            if np.array_equal(self.garden, self.new_garden):
                return i+1
            self.garden = self.new_garden
            if print_garden:
                print(f' == End of Round {i + 1}')
                self.print()
        return n

    def single_elf_propose(self, index, direction_idx):
        ordered_direction_checks = self.check_directions_for_elf(direction_idx, index)

        # Checking if everything around is clear, if so, not proposing anything
        if sum(check[0] for check in ordered_direction_checks) == 4:
            return

        for check, proposed_position in ordered_direction_checks:
            if check:
                # Adding our proposal
                self.proposed_moves[proposed_position] += 1
                return

    def single_elf_move(self, index, direction_idx):
        ordered_direction_checks = self.check_directions_for_elf(direction_idx, index)

        # Checking if everything around is clear, if so, staying stationary
        if sum(check[0] for check in ordered_direction_checks) == 4:
            self.new_garden[index] = 1
            return

        for check, proposed_position in ordered_direction_checks:
            if check:
                if self.proposed_moves[proposed_position] == 1:
                    # Actually moving since we are the only proposal
                    self.new_garden[proposed_position] = 1
                    return

                else:
                    # Our proposal isn't unique, leaving
                    break

        # Can't move, staying stationary
        self.new_garden[index] = 1
        return

    def check_directions_for_elf(self, direction_idx, index):
        direction_checks = [
            # North
            (sum(self.garden[index[0] - 1, index[1] - 1:index[1] + 2]) == 0, (index[0] - 1, index[1])),
            # South
            (sum(self.garden[index[0] + 1, index[1] - 1:index[1] + 2]) == 0, (index[0] + 1, index[1])),
            # West
            (sum(self.garden[index[0] - 1:index[0] + 2, index[1] - 1]) == 0, (index[0], index[1] - 1)),
            # East
            (sum(self.garden[index[0] - 1:index[0] + 2, index[1] + 1]) == 0, (index[0], index[1] + 1)),
        ]
        ordered_direction_checks = direction_checks[direction_idx:] + direction_checks[:direction_idx]
        return ordered_direction_checks

    def print(self):
        with open('garden.txt', 'w') as f:
            print()
            for row in self.garden:
                row_str = ''
                for t in row:
                    row_str += '#' if t else '.'
                f.write(f'{row_str}\n')
                print(f'{row_str}')

    def trim_garden_to_box(self):
        xs = []
        ys = []
        for index, p in np.ndenumerate(self.garden):
            if p == 1:
                xs.append(index[1])
                ys.append(index[0])
        trimmed_garden = self.garden[min(ys):max(ys) + 1, min(xs):max(xs) + 1]
        self.garden = trimmed_garden


class Day23(AdventOfCodePuzzle):

    def part_1(self, inputs: List[str]):
        garden = ElfGarden(inputs)

        garden.propose_and_move(10)
        garden.trim_garden_to_box()

        garden.print()
        return (garden.garden == 0).sum()

    def part_2(self, inputs: List[str]):
        garden = ElfGarden(inputs)

        return garden.propose_and_move(1100)
