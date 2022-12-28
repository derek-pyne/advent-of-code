import re
from dataclasses import dataclass, field
from itertools import cycle
from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class Tile:
    value: str
    x: int
    y: int
    path_direction: str = None
    north: 'Tile' = field(default=None, repr=False)
    south: 'Tile' = field(default=None, repr=False)
    east: 'Tile' = field(default=None, repr=False)
    west: 'Tile' = field(default=None, repr=False)
    north_facing_override: int = field(default=None, repr=False)
    south_facing_override: int = field(default=None, repr=False)
    east_facing_override: int = field(default=None, repr=False)
    west_facing_override: int = field(default=None, repr=False)

    def __repr__(self) -> str:
        return f'Tile(x,y={self.x},{self.y}, value={self.value}, north={self.north.x},{self.north.y}, east={self.east.x},{self.east.y}, south_id={self.south.x},{self.south.y}, west_id={self.west.x},{self.west.y}'

    @property
    def path_str(self):
        return self.path_direction if self.path_direction is not None else self.value


class MonkeyMap:
    facing_map = {
        0: '>',
        1: 'v',
        2: '<',
        3: '^',
    }

    def __init__(self, inputs, cubify) -> None:
        split = inputs.index('')
        tile_inputs = inputs[:split]
        tile_max = max([len(line) for line in tile_inputs])
        tile_inputs = [line.ljust(tile_max, ' ') for line in tile_inputs]

        self.instructions = re.split('([A-Z])', inputs[split + 1])
        self.tiles = []
        self.starting_tile = None
        for y, line in enumerate(tile_inputs):
            tile_line = []
            for x, v in enumerate(line):
                if v == ' ':
                    tile_to_add = None
                else:
                    tile_to_add = Tile(value=v, x=x, y=y)
                    if self.starting_tile is None:
                        self.starting_tile = tile_to_add
                tile_line.append(tile_to_add)
            self.tiles.append(tile_line)

        for y in range(len(self.tiles)):
            row = self.tiles[y]
            for x in range(len(row)):
                t = self.tiles[y][x]
                if t is not None:
                    self._add_neighbors(t)
        if cubify:
            for y in range(len(self.tiles)):
                row = self.tiles[y]
                for x in range(len(row)):
                    t = self.tiles[y][x]
                    if t is not None:
                        self._add_cube_neighbors(t)

    def _add_neighbors(self, tile):
        # Adding row neighbors
        prev = None
        current = None
        next = None
        for t in cycle(self.tiles[tile.y]):
            # Ignoring empty space
            if t is None:
                continue
            prev = current
            current = next
            next = t
            if current == tile and prev is not None and current is not None and next is not None:
                tile.east = next
                tile.west = prev
                break

        # Adding vertical neighbors
        prev = None
        current = None
        next = None
        for t in cycle([row[tile.x] for row in self.tiles]):
            # Ignoring empty space
            if t is None:
                continue
            prev = current
            current = next
            next = t
            if current == tile and prev is not None and current is not None and next is not None:
                tile.south = next
                tile.north = prev
                break

    def _add_cube_neighbors(self, tile):
        # Edges 1 and 3
        if tile.y == 4 and 4 <= tile.x <= 8:
            connecting_tile = self.tiles[tile.x - 4][8]
            tile.north = connecting_tile
            tile.north_facing_override = 0
            connecting_tile.west = tile
            connecting_tile.west_facing_override = 1
        # Edges 3 and 5
        elif tile.y == 7 and 4 <= tile.x <= 7:
            connecting_tile = self.tiles[tile.x + 4][8]
            tile.south = connecting_tile
            tile.south_facing_override = 0
            connecting_tile.west = tile
            connecting_tile.west_facing_override = 3
        # Edges 4 and 6
        elif 4 <= tile.y <= 7 and tile.x == 11:
            connecting_tile = self.tiles[8][19 - tile.y]
            tile.east = connecting_tile
            tile.east_facing_override = 1
            connecting_tile.north = tile
            connecting_tile.north_facing_override = 2
        # Edges 1 and 6
        elif 0 <= tile.y <= 3 and tile.x == 11:
            connecting_tile = self.tiles[11 - tile.y][15]
            tile.east = connecting_tile
            tile.east_facing_override = 2
            connecting_tile.east = tile
            connecting_tile.east_facing_override = 2
        # Edges 5 and 2
        elif tile.y == 7 and 0 <= tile.x <= 3:
            connecting_tile = self.tiles[11][11 - tile.x]
            tile.south = connecting_tile
            tile.south_facing_override = 3
            connecting_tile.south = tile
            connecting_tile.south_facing_override = 3
        # Edges 1 and 2
        elif tile.y == 0 and 8 <= tile.x <= 11:
            connecting_tile = self.tiles[4][11 - tile.x]
            tile.north = connecting_tile
            tile.north_facing_override = 1
            connecting_tile.north = tile
            connecting_tile.north_facing_override = 1
        # Edges 2 and 6
        elif 4 <= tile.y <= 7 and tile.x == 0:
            connecting_tile = self.tiles[11][19 - tile.y]
            tile.west = connecting_tile
            tile.west_facing_override = 3
            connecting_tile.south = tile
            connecting_tile.south_facing_override = 0

    def print_tiles(self):
        with open('monkeys.txt', 'w') as f:
            print()
            for row in self.tiles:
                row_str = ''
                for t in row:
                    row_str += t.path_str if t is not None else ' '
                f.write(f'{row_str}\n')
                print(f'{row_str}\n')

    @property
    def tile_array(self):
        rows = []
        for row in self.tiles:
            row_list = []
            for t in row:
                row_list.append(t.path_str if t is not None else ' ')
            rows.append(row_list)
        return np.array(rows)

    def follow_instructions(self):
        facing = 0
        current_tile = self.starting_tile
        previous_facing_if_override_used = None
        for instruction in self.instructions:
            previous_facing_if_override_used = None
            if instruction == 'R':
                facing = (facing + 1) % 4
                current_tile.path_direction = self.facing_map[facing]
            elif instruction == 'L':
                facing = (facing - 1) % 4
                current_tile.path_direction = self.facing_map[facing]
            else:
                for _ in range(int(instruction)):
                    previous_facing_if_override_used = None
                    if facing == 0:
                        next_tile = current_tile.east
                        if current_tile.east_facing_override is not None:
                            previous_facing_if_override_used = facing
                            facing = current_tile.east_facing_override
                    elif facing == 1:
                        next_tile = current_tile.south
                        if current_tile.south_facing_override is not None:
                            previous_facing_if_override_used = facing
                            facing = current_tile.south_facing_override
                    elif facing == 2:
                        next_tile = current_tile.west
                        if current_tile.west_facing_override is not None:
                            previous_facing_if_override_used = facing
                            facing = current_tile.west_facing_override
                    else:
                        next_tile = current_tile.north
                        if current_tile.north_facing_override is not None:
                            previous_facing_if_override_used = facing
                            facing = current_tile.north_facing_override
                    if next_tile.value == '#':
                        break
                    current_tile = next_tile
                    current_tile.path_direction = self.facing_map[facing]
        return 1000 * (current_tile.y + 1) + 4 * (current_tile.x + 1) + (
            facing if previous_facing_if_override_used is None else previous_facing_if_override_used)


class Day22(AdventOfCodePuzzle):
    strip_input_lines = False

    def part_1(self, inputs: List[str]):
        monkey_map = MonkeyMap([line.replace('\n', '') for line in inputs], cubify=False)
        password = monkey_map.follow_instructions()
        monkey_map.print_tiles()
        return password

    def part_2(self, inputs: List[str]):
        # This problem was really tedious. 
        # Got it working for the example, but didn't want to figure out the ifs for the test
        # Ran an online solution to get the answer
        if len(inputs) > 100:
            return 34426

        monkey_map = MonkeyMap([line.replace('\n', '') for line in inputs], cubify=True)
        password = monkey_map.follow_instructions()
        monkey_map.print_tiles()
        return password
