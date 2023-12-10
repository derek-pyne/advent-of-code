import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Node:
    x: int
    y: int
    char: str
    distance: int = None
    

nodes = []
with open(os.path.join(os.path.dirname(__file__), 'inputs/day_10.txt')) as f:
    
    starting_node = None
    for y, line in enumerate(f.readlines()):
        node_line = []
        line = line.strip()
        for x, c in enumerate(line):
            node = Node(x=x, y=y, char=c)
            if c == 'S':
                starting_node = node
            node_line.append(node)
        nodes.append(node_line)
range_y = len(nodes)
range_x = len(nodes[0])

starting_node.distance = 0
nodes_to_check = [starting_node]

# Dijkstra
while len(nodes_to_check) > 0:
    # Removing closest node
    n = nodes_to_check.pop(0)
    
    possibles = []
    # Check all neighbors of n
    # North
    if n.char in '|LJS' and (n.y-1) >=0:
        possible = nodes[n.y-1][n.x]
        if possible.distance is None and possible.char in '|F7':
            possibles.append(possible)
    # South
    if n.char in '|7FS' and (n.y+1) < range_y:
        possible = nodes[n.y+1][n.x]
        if possible.distance is None and possible.char in '|LJ':
            possibles.append(possible)
    # East
    if n.char in '-LFS' and (n.x+1) < range_x:
        possible = nodes[n.y][n.x+1]
        if possible.distance is None and possible.char in '-7J':
            possibles.append(possible)
    # West
    if n.char in '-7JS' and (n.x-1) >=0:
        possible = nodes[n.y][n.x-1]
        if possible.distance is None and possible.char in '-LF':
            possibles.append(possible)
    
    for p in possibles:
        if p.distance is None:
            p.distance = n.distance+1
            nodes_to_check.append(p)

print(max(n.distance for line in nodes for n in line if n.distance is not None))
