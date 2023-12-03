import operator
from functools import reduce

with open('src/year_2020/inputs/day3.txt') as f:
    grid = [x.strip() for x in f.readlines()]


def trees_hit(dx, dy):
    x = 0
    y = 0
    width = len(grid[0])
    trees = 0
    while True:
        x += dx
        y += dy
        if y >= len(grid):
            break
        trees += grid[y][x % width] == '#'
    return trees


print(f'Part 1: {trees_hit(dx=3, dy=1)}')

args = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
print(f'Part 2: {reduce(operator.mul, [trees_hit(*slopes) for slopes in args])}')
