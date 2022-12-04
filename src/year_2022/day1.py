from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


def get_inventories(inputs):
    inventories = []
    current_inventory = []
    for line in inputs:
        if len(line) != 0:
            # Adding to existing elfs inventory
            current_inventory.append(int(line))
        else:
            # Closing out this elfs inventory and creating a fresh one
            inventories.append(current_inventory)
            current_inventory = []
    inventories.append(current_inventory)

    total_inventories = [sum(i) for i in inventories]
    total_inventories.sort(reverse=True)
    return total_inventories


class Day1(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        total_inventories = get_inventories(inputs=inputs)
        return total_inventories[0]

    def part_2(self, inputs: List[str]) -> int:
        total_inventories = get_inventories(inputs=inputs)
        return sum(total_inventories[:3])
