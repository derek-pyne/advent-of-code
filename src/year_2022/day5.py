import re
from dataclasses import dataclass
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class Instruction:
    start_stack: int
    end_stack: int
    quantity: int


def parse_instructions(inputs: List[str]):
    # Parsing stacks

    stacks = [[]]
    for line in inputs:
        for match in re.finditer('\[([A-Z]*)\]', line):

            stack_index = int(match.start() / 4)

            # Adding new stack if needed
            while len(stacks) <= stack_index:
                stacks.append([])

            # Putting crate at beginning of stack
            stacks[stack_index].insert(
                0,
                re.match('\[([A-Z]*)\]', match.group()).groups()[0],
            )

    instructions = []
    for line in inputs:
        match = re.match('move (\d*) from (\d*) to (\d*)', line)
        if match is not None:
            instructions.append(Instruction(
                quantity=int(match.groups()[0]),
                start_stack=int(match.groups()[1]) - 1,
                end_stack=int(match.groups()[2]) - 1,
            ))
    return stacks, instructions


def follow_instructions_9000(stacks, instructions):
    for n, instruction in enumerate(instructions):
        for i in range(instruction.quantity):
            if len(stacks[instruction.start_stack]) == 0:
                break
            stacks[instruction.end_stack].append(stacks[instruction.start_stack].pop())

    return stacks


def follow_instructions_9001(stacks, instructions):
    for n, instruction in enumerate(instructions):
        moved_crates = []
        for i in range(instruction.quantity):
            if len(stacks[instruction.start_stack]) == 0:
                break
            moved_crates.append(stacks[instruction.start_stack].pop())
        stacks[instruction.end_stack].extend(moved_crates[::-1])

    return stacks


class Day5(AdventOfCodePuzzle):
    strip_input_lines = False

    def part_1(self, inputs: List[str]):
        stacks, instructions = parse_instructions(inputs)
        stacks = follow_instructions_9000(stacks, instructions)
        return ''.join([s[-1] if len(s) else ' ' for s in stacks])

    def part_2(self, inputs: List[str]):
        stacks, instructions = parse_instructions(inputs)
        stacks = follow_instructions_9001(stacks, instructions)
        return ''.join([s[-1] if len(s) else ' ' for s in stacks])
