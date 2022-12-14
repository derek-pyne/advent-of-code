import itertools
from dataclasses import field, dataclass
from heapq import heappop, heappush
from typing import List

import numpy as np

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class PriorityQueue:
    REMOVED = '<removed-task>'  # placeholder for a removed task

    def __init__(self) -> None:
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self, ):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')


@dataclass(order=True, unsafe_hash=True)
class Node:
    tentative_distance: int = field(hash=False)
    x: int = field(compare=False, hash=True)
    y: int = field(compare=False, hash=True)


def minimum_risks(risks):
    visited = np.zeros_like(risks, dtype=bool)
    y_lim, x_lim = risks.shape

    node_queue = PriorityQueue()
    tentative_distance = np.zeros_like(risks, dtype=Node)
    for x in range(0, x_lim):
        for y in range(0, y_lim):
            node = Node(tentative_distance=9999999999, x=x, y=y)
            tentative_distance[y, x] = node
            node_queue.add_task(task=node, priority=node.tentative_distance)

    root_node = tentative_distance[0, 0]
    root_node.tentative_distance = 0
    node_queue.add_task(task=root_node, priority=root_node.tentative_distance)

    current_node = root_node

    while True:
        possible_neighbors = [
            (current_node.x - 1, current_node.y),
            (current_node.x + 1, current_node.y),
            (current_node.x, current_node.y - 1),
            (current_node.x, current_node.y + 1),
        ]
        for x, y in possible_neighbors:
            if (0 <= x <= x_lim - 1) and (0 <= y <= y_lim - 1) and not visited[y, x]:
                new_distance = risks[y, x] + current_node.tentative_distance
                node = tentative_distance[y, x]
                if new_distance < node.tentative_distance:
                    node.tentative_distance = new_distance
                    node_queue.add_task(task=node, priority=node.tentative_distance)

        try:
            current_node = node_queue.pop_task()
        except KeyError:
            return tentative_distance


def increase_risk(risk, increase_by):
    new_risk = risk.copy()
    for _ in range(increase_by):
        new_risk += 1
        new_risk = np.where(new_risk <= 9, new_risk, 1)
    return new_risk


class Day15(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        risks = np.array([[int(x) for x in line] for line in inputs])
        min_risks = minimum_risks(risks)
        return min_risks[-1, -1].tentative_distance

    def part_2(self, inputs: List[str]):
        risks = np.array([[int(x) for x in line] for line in inputs])
        h_risk_list = [increase_risk(risks, i) for i in range(5)]
        row = np.hstack(h_risk_list)

        v_risk_list = [increase_risk(row, i) for i in range(5)]
        big_risk = np.vstack(v_risk_list)

        min_risks = minimum_risks(big_risk)
        return min_risks[-1, -1].tentative_distance
