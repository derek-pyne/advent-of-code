import copy
from collections import defaultdict
from typing import List, Dict

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class SubmarinePath:

    def __init__(self, cave_connections: Dict, double_up_single_small_cave=False) -> None:
        self.nodes_visited = []
        self.path = ['start']
        self.cave_connections = cave_connections
        self.double_up_single_small_cave = double_up_single_small_cave

    def __repr__(self) -> str:
        return f"SubmarinePath({' -> '.join(self.path)}"

    @property
    def current_node(self):
        return self.path[-1]

    @property
    def is_complete(self):
        return self.current_node == 'end'

    def can_travel_to(self, node):
        if node == 'start':
            return False
        elif node == 'end':
            return True
        elif node not in self.small_caves_visited:
            return True
        elif self.double_up_single_small_cave and len(set(self.small_caves_visited)) == len(self.small_caves_visited):
            return True
        return False

    @property
    def small_caves_visited(self) -> List[str]:
        return [p for p in self.path if p not in ['start', 'end'] and p.islower()]

    def split_into_new_paths(self) -> List['SubmarinePath']:
        possibilities = self.cave_connections[self.path[-1]]

        sps = []
        for option in possibilities:
            if self.can_travel_to(option):
                new_path = copy.deepcopy(self)
                new_path.path.append(option)
                if new_path.is_complete:
                    sps.append(new_path)
                else:
                    sps.extend(new_path.split_into_new_paths())
        return sps


class Day12(AdventOfCodePuzzle):
    @staticmethod
    def parse_cave_connections(inputs):
        d = defaultdict(list)
        for line in inputs:
            start, end = line.split('-')
            d[start].append(end)
            d[end].append(start)
        return d

    def part_1(self, inputs: List[str]):
        d = self.parse_cave_connections(inputs)
        paths = SubmarinePath(cave_connections=d).split_into_new_paths()
        return len([p for p in paths if len(p.small_caves_visited) > 0])

    def part_2(self, inputs: List[str]):
        d = self.parse_cave_connections(inputs)
        paths = SubmarinePath(cave_connections=d, double_up_single_small_cave=True).split_into_new_paths()
        return len(paths)
