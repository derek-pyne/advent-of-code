from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class PolymerPairs:
    pairs: Dict[str, int]
    insertion_map: Dict[str, str]

    def insert(self):
        changes = []
        for pair, count in self.pairs.items():
            if pair in self.insertion_map:
                changes.extend([
                    (pair, -count),
                    (pair[0] + self.insertion_map[pair], count),
                    (self.insertion_map[pair] + pair[1], count),
                ])
        for key, val in changes:
            self.pairs[key] += val

    def character_counts(self) -> Dict[str, int]:
        counts = defaultdict(int)
        for pair, count in self.pairs.items():
            counts[pair[0]] += count
        return counts


def parse_input(inputs):
    polymer = inputs[0] + 'X'
    polymer_pairs = defaultdict(int)
    for i in range(len(polymer) - 1):
        polymer_pairs[polymer[i:i + 2]] += 1
    insertions = {}
    for line in inputs[2:]:
        pair, insert = line.split(' -> ')
        insertions[pair] = insert
    return PolymerPairs(pairs=polymer_pairs, insertion_map=insertions)


class Day14(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        pp = parse_input(inputs)
        for i in range(10):
            pp.insert()

        return max(pp.character_counts().values()) - min(pp.character_counts().values())

    def part_2(self, inputs: List[str]):
        pp = parse_input(inputs)
        for i in range(40):
            pp.insert()

        return max(pp.character_counts().values()) - min(pp.character_counts().values())
