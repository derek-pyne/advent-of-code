import os
import re


def is_game_possible(line) -> int:
    match = re.match('Game (\d+):', line)
    id = int(match.groups()[0])
    cubes = [
        ('red', 12),
        ('green', 13),
        ('blue', 14),
        ]
    power = 1
    for color, max_cube in cubes:
        cube_counts = re.findall('(\d+) '+color, line)
        cube_counts = [int(x) for x in cube_counts]
        # if any([int(x) > max_cube for x in cube_counts]):
        #     return 0
        min_cubes = max(cube_counts)
        print(f'Min {color} is {min_cubes}')
        power *= min_cubes
    print(f'Power: {power}')
    return power

with open(os.path.join(os.path.dirname(__file__), 'inputs/day_2.txt')) as f:
    sum = 0
    for line in f.readlines():
        sum += is_game_possible(line.strip())
    print(sum)
