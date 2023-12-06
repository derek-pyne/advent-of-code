import math
import os
import re


def solve_quadratic(a, b, c):
    # calculate the discriminant
    d = (b ** 2) - (4 * a * c)

    # find two solutions
    sol1 = (-b - math.sqrt(d)) / (2 * a)
    sol2 = (-b + math.sqrt(d)) / (2 * a)

    return sol1, sol2


with open(os.path.join(os.path.dirname(__file__), 'inputs/day_6.txt')) as f:
    times = re.findall(r'\d+', f.readline())
    target_distances = re.findall(r'\d+', f.readline())


# distance = (time - wait) * wait
# distance =  - wait * 2 + time * wait
# a= -1, b = time, c = - (target_distance+1)

def boat_race(times, target_distances):
    ans = 1
    for t, d in zip(times, target_distances):
        large_sol, small_sol = solve_quadratic(-1, int(t), -(int(d) + 1))
        possibilities = math.floor(large_sol) - math.ceil(small_sol) + 1
        # print(large_sol, small_sol)
        # print(possibilities)
        ans *= possibilities
    return ans


print(f'Part 1: {boat_race(times, target_distances)}')

# Part 2
times = [''.join(times)]
target_distances = [''.join(target_distances)]
print(f'Part 2: {boat_race(times, target_distances)}')
