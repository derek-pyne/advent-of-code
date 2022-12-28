import re
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


# Toooo hard, total copy of https://www.youtube.com/watch?v=H3PSODv4nf0&t=351s

class RobotFactory:

    def __init__(self, inputs) -> None:
        self.inputs = inputs

    def compute(self, time_remaining):

        part1_total = 0
        part2_total = 1
        for i, line in enumerate(self.inputs):
            bp = []

            # Optimization: We keep track of the maximum that you can possibly spend of each resource (except geode)
            # each round. There is no point in making more robots of a resource then the maximum you can spend a turn
            maxspend = [0, 0, 0]
            for section in line.split(': ')[1].split('. '):
                recipe = []
                for x, y in re.findall('(\d+) (\w+)', section):
                    x = int(x)
                    y = ['ore', 'clay', 'obsidian'].index(y)
                    recipe.append((x, y))
                    maxspend[y] = max(maxspend[y], x)
                bp.append(recipe)
            v = self.dfs(bp, maxspend, {}, time_remaining, [1, 0, 0, 0], [0, 0, 0, 0])
            part1_total += (i + 1) * v
            part2_total *= v
        return part1_total, part2_total

    def dfs(self, bp, maxspend, cache, time, bots, amt):
        if time == 0:
            return amt[3]

        key = tuple([time, *bots, *amt])
        if key in cache:
            return cache[key]

        # Do nothing case, just sit, and get geodes based on current geode robots
        maxval = amt[3] + bots[3] * time

        # Wait for enough resources and build a robot of each type
        for btype, recipe in enumerate(bp):
            # Don't build robot if already at maxspend (except for geode)
            if btype != 3 and bots[btype] >= maxspend[btype]:
                continue

            wait = 0
            for ramt, rtype in recipe:
                # If we don't have any bots of the needed resource, no matter how long we wait we won't collect enough
                if bots[rtype] == 0:
                    break
                # Hack for ceiling division
                wait = max(wait, -(-(ramt - amt[rtype]) // bots[rtype]))
            else:
                remtime = time - wait - 1

                # Skipping if there is not time for this robot to actually make a resource
                if remtime <= 0:
                    continue

                bots_ = bots[:]
                amt_ = [x + y * (wait + 1) for x, y in zip(amt, bots)]
                for ramt, rtype in recipe:
                    amt_[rtype] -= ramt
                bots_[btype] += 1

                # Optimization, throwing away extra unneeded resources to help the cache hit more often
                for i in range(3):
                    amt_[i] = min(amt_[i], maxspend[i] * remtime)
                maxval = max(maxval, self.dfs(bp, maxspend, cache, remtime, bots_, amt_))

        cache[key] = maxval
        return maxval


class Day19(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        return RobotFactory(inputs).compute(time_remaining=24)[0]

    def part_2(self, inputs: List[str]):
        return RobotFactory(inputs[:3]).compute(time_remaining=32)[1]
