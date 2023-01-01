import re
from typing import List, Tuple

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class ProbeShooter:

    def __init__(self, inputs) -> None:
        match = re.match(
            'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)',
            inputs[0]
        )
        self.target_x_min = int(match.groups()[0])
        self.target_x_max = int(match.groups()[1])
        self.target_y_min = int(match.groups()[2])
        self.target_y_max = int(match.groups()[3])

    def shoot_probe(self, x_vel, y_velo) -> Tuple[bool, int]:
        x = 0
        y = 0
        max_y = y
        while x <= self.target_x_max and y >= self.target_y_min:
            if self.target_x_min <= x <= self.target_x_max and self.target_y_min <= y <= self.target_y_max:
                return True, max_y

            x += x_vel
            y += y_velo
            if x_vel != 0:
                x_vel += 1 if x_vel < 0 else -1

            y_velo -= 1
            max_y = max(max_y, y)
        return False, max_y

    def highest_shot(self):

        max_y = 0
        # [Necessary] x_vel must be small enough that there is at least one point within the x range
        # [Optimization] x_vel must be large enough to make it to the border of the x_min
        max_test_x_vel = self.target_x_max + 1
        max_test_y_vel = abs(self.target_y_min - 1)
        for test_x_vel in range(0, max_test_x_vel):
            # [Necessary] y_vel must be less than y min so that there is at least one within y range
            for test_y_vel in range(0, max_test_y_vel):
                success, shot_max_y = self.shoot_probe(test_x_vel, test_y_vel)
                if success:
                    max_y = max(max_y, shot_max_y)
        return max_y

    def all_possible_shots(self) -> List:
        max_y = 0
        # [Necessary] x_vel must be small enough that there is at least one point within the x range
        # [Optimization] x_vel must be large enough to make it to the border of the x_min
        max_test_x_vel = self.target_x_max + 1
        max_test_y_vel = abs(self.target_y_min - 1)
        min_test_y_vel = self.target_y_min - 1
        shots = []
        for test_x_vel in range(0, max_test_x_vel):
            # [Necessary] y_vel must be less than y min so that there is at least one within y range
            for test_y_vel in range(min_test_y_vel, max_test_y_vel):
                success, shot_max_y = self.shoot_probe(test_x_vel, test_y_vel)
                if success:
                    shots.append((test_x_vel, test_y_vel))
        return shots


class Day17(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        shooter = ProbeShooter(inputs)
        return shooter.highest_shot()

    def part_2(self, inputs: List[str]):
        shooter = ProbeShooter(inputs)
        shots = shooter.all_possible_shots()
        return len(shots)
