import math
from collections import deque
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


# Essentially a copy of: https://www.youtube.com/watch?v=R_QWG-cPp_k
class BlizzardRunner:

    def __init__(self, inputs) -> None:
        self.blizzards = [set() for _ in range(4)]
        self.y_len = len(inputs) - 2
        self.x_len = len(inputs[0]) - 2
        for y, line in enumerate(inputs[1:]):
            for x, c in enumerate(line[1:]):
                if c in '<>^v':
                    self.blizzards['<>^v'.find(c)].add((x, y))

    def find_path_out(self):
        return self.find_path(targets=[(self.x_len - 1, self.y_len)])

    def find_path_out_while_grabbing_snacks(self):
        return self.find_path(targets=[(self.x_len - 1, self.y_len), (0, -1), (self.x_len - 1, self.y_len)])

    def find_path(self, targets):

        initial = (0, 0, -1, 0)
        seen = set()

        q = deque([initial])

        # Blizzard repeats itself in a cycle
        lcm = self.x_len * self.y_len // math.gcd(self.x_len, self.y_len)

        while q:
            time, x, y, stage = q.popleft()
            time += 1

            # Looking at possible next moves
            for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x, y)]:

                nstage = stage
                if (nx, ny) == targets[stage]:
                    if stage == len(targets) - 1:
                        return time
                    nstage += 1

                if (nx < 0 or ny < 0 or nx >= self.x_len or ny >= self.y_len) and (nx, ny) not in targets and (
                        nx, ny) != (0, -1):
                    continue

                # Checking blizzards by moving our position in the opposite direction that the blizzard is travelling
                hit_blizzard = False
                if (nx, ny) not in targets and (nx, ny) != (0, -1):
                    for i, test_x, test_y in [(0, -1, 0), (1, 1, 0), (2, 0, -1), (3, 0, 1)]:
                        if ((nx - test_x * time) % self.x_len, (ny - test_y * time) % self.y_len) in self.blizzards[i]:
                            hit_blizzard = True
                            break

                if not hit_blizzard:
                    key = (nx, ny, time % lcm, nstage)

                    if key in seen:
                        continue
                    seen.add(key)
                    q.append((time, nx, ny, nstage))
        return -1


class Day24(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        return BlizzardRunner(inputs).find_path_out()

    def part_2(self, inputs: List[str]):
        return BlizzardRunner(inputs).find_path_out_while_grabbing_snacks()
