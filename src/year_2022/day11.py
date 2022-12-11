from dataclasses import dataclass, field
from functools import reduce
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle
from src.utils import grouper


@dataclass
class Monkey:
    items: List[int]
    operation_command: str
    divisor: int
    true_pass: int
    false_pass: int
    inspection_count: int = field(default=0, init=False)
    lcm: int = field(default=0, init=False)

    def process_items(self, use_lcm=False):
        items_to_through = self.items
        self.items = []
        for item in items_to_through:
            new_worry = self.operate(worry=item)
            if use_lcm:
                new_worry = new_worry % self.lcm
            else:
                new_worry = new_worry // 3
            if self.test(new_worry):
                yield self.true_pass, new_worry
            else:
                yield self.false_pass, new_worry

    def operate(self, worry):
        self.inspection_count += 1
        old = worry
        new = eval(self.operation_command.split('new = ')[1])
        return new

    def test(self, worry):
        return (worry % self.divisor) == 0


@dataclass
class MonkeyGames:
    monkeys: List[Monkey]

    def __post_init__(self):
        lcm = reduce(lambda x, y: x * y, [m.divisor for m in self.monkeys])
        for m in self.monkeys:
            m.lcm = lcm

    def round(self, use_lcm=False):
        for m in self.monkeys:
            for target, item in m.process_items(use_lcm=use_lcm):
                self.monkeys[target].items.append(item)

    def print_items(self):
        for i, m in enumerate(self.monkeys):
            print(f'Monkey {i}: {", ".join([str(item) for item in m.items])}')

    def inspection_counts(self):
        return [m.inspection_count for m in self.monkeys]

    def multiplied_top_two_inspection_counts(self):
        counts = self.inspection_counts()
        counts.sort(reverse=True)
        return counts[0] * counts[1]


class Day11(AdventOfCodePuzzle):

    @staticmethod
    def parse_monkey_input(inputs):
        monkeys = []
        for g in grouper(inputs, n=7):
            monkeys.append(Monkey(
                items=[int(x) for x in g[1].split(': ')[1].split(', ')],
                operation_command=g[2].split(': ')[1],
                divisor=int(g[3].split('divisible by ')[1]),
                true_pass=int(g[4].split('monkey ')[1]),
                false_pass=int(g[5].split('monkey ')[1]),
            ))
        game = MonkeyGames(monkeys=monkeys)
        return game

    def part_1(self, inputs: List[str]):
        game = self.parse_monkey_input(inputs)
        print()
        for i in range(20):
            print(f'After round {i + 1},')
            game.round()
            game.print_items()
            print()

        return game.multiplied_top_two_inspection_counts()

    def part_2(self, inputs: List[str]):
        game = self.parse_monkey_input(inputs)
        for i in range(10000):
            game.round(use_lcm=True)

        return game.multiplied_top_two_inspection_counts()
