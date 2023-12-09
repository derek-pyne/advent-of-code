import os

nodes = {}
with open(os.path.join(os.path.dirname(__file__), 'inputs/day_8.txt')) as f:
    lines = f.readlines()
    lr = lines[0].strip()
    for line in lines[2:]:
        key, val = line.split(' = ')
        
        nodes[key] = val.strip().replace('(', "").replace(')', "").split(', ')

i = 0
currents = [n for n in nodes.keys() if n.endswith('A')]

lcm_vals = []
while True:
    # print(currents)
    direction = lr[i % len(lr)]
    for n in range(len(currents)):
        if direction == 'L':
            currents[n] = nodes[currents[n]][0]
        elif direction == 'R':
            currents[n] = nodes[currents[n]][1]
        else:
            raise ValueError(f'Direction : {direction}')
        if currents[n].endswith('Z'):
            lcm_vals.append(i+1)
    i += 1
    if len(currents) == len(lcm_vals):
        break

import math
from functools import reduce  # Importing reduce to apply lcm function over the list

# Function to return the LCM of two numbers
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

# Function to find LCM of all numbers in a list
def lcm_list(numbers):
    return reduce(lcm, numbers)
print(f'Steps: {lcm_list(lcm_vals)}')
    
