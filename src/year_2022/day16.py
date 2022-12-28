import re
from collections import deque
from dataclasses import dataclass, field
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


# Toooo tough for me
# Essentially a copy of https://www.youtube.com/watch?v=bLMj50cpOug
# Except I made it worse by adding a Valve class

@dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels_raw: List[str]
    tunnels: List['Valve'] = field(default_factory=list, repr=False)


class ValveOpener:
    def __init__(self, inputs) -> None:
        self.valves = {}
        for line in inputs:
            match = re.match('Valve ([A-Z]{2}) has flow rate=(\d*); tunnels? leads? to valves? (.*)', line)
            if not match:
                raise ValueError(f'Failed to parse: {line}')

            tunnels_raw = match.groups()[2].split(', ')
            name = match.groups()[0]
            self.valves[name] = Valve(
                name=name,
                flow_rate=int(match.groups()[1]),
                tunnels_raw=tunnels_raw,
            )

        # Adding connections
        for valve in self.valves.values():
            valve.tunnels = [self.valves[v] for v in valve.tunnels_raw]

        # Want to only look at paths to valves with non-zero flow rate
        # This compresses our graph hugely
        self.dists = {}
        self.nonempty_valves = []
        for valve in self.valves.values():
            if valve.name != 'AA' and valve.flow_rate == 0:
                continue

            if valve.name != 'AA':
                self.nonempty_valves.append(valve.name)

            self.dists[valve.name] = {valve.name: 0, 'AA': 0}

            # Doing BFS to find shortest path between current valve and all other non-zero flowrate valves
            queue = deque([(0, valve.name)])
            visited = {valve.name}

            while queue:
                distance, position = queue.popleft()
                for neighbor in self.valves[position].tunnels_raw:
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)
                    if self.valves[neighbor].flow_rate != 0:
                        self.dists[valve.name][neighbor] = distance + 1
                    queue.append((distance + 1, neighbor))

            # Deleting paths to self and AA since AA is blocked
            del self.dists[valve.name][valve.name]
            if valve.name != 'AA':
                del self.dists[valve.name]['AA']

        self.indices = {}
        for i, element in enumerate(self.nonempty_valves):
            self.indices[element] = i

        self.cache = {}

    def dfs(self, time, valve_name, bitmask):
        # Doing DFS with a cache to speed it up
        # Using a bitmask to represent which valves are on and off
        if (time, valve_name, bitmask) in self.cache:
            return self.cache[(time, valve_name, bitmask)]
        maxval = 0
        for neighbor in self.dists[valve_name]:
            bit = 1 << self.indices[neighbor]

            # If the valve is already open in the bitmask, no need to go and open it
            if bitmask & bit:
                continue

            # This is the amount of remaining time after we travel to this neighbor and open the valve
            remaining_time = time - self.dists[valve_name][neighbor] - 1

            # If we don't have enough time to travel and open the valve, no point in doing this
            if remaining_time <= 0:
                continue

            # Adding how much flow would be gained if valve was open for the remaining time
            maxval = max(maxval,
                         self.dfs(remaining_time, neighbor, bitmask | bit) + self.valves[
                             neighbor].flow_rate * remaining_time)

        self.cache[(time, valve_name, bitmask)] = maxval
        return maxval


class Day16(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        return ValveOpener(inputs=inputs).dfs(30, 'AA', 0)

    def part_2(self, inputs: List[str]):
        v = ValveOpener(inputs=inputs)

        # Now that we have two workers, we'll partition the valves into two sections
        # Essentially, we are solving for each worker, and pretending that the other worker had already opened their valves
        # Since our dfs actually calculates the ADDED flow rate from a path, this works out for us

        # All valves on
        b = (1 << len(v.nonempty_valves)) - 1

        maxval = 0
        for i in range(b + 1):
            # The xor gets us the complement
            maxval = max(maxval, v.dfs(26, 'AA', i) + v.dfs(26, 'AA', i ^ b))

        return maxval
