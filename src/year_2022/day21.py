import re
from typing import List, Dict, Union

from attr import dataclass
from sympy import Eq, symbols, solve, parse_expr

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class Monkey:
    name: str
    operation: str
    dependencies: set[str]
    value: Union[int, str] = None

    def run_operation(self, dependency_values: Dict[str, int], attempt_eval=True) -> bool:
        if self.dependencies != set(dependency_values.keys()):
            return False

        op = self.operation
        for name, value in dependency_values.items():
            op = op.replace(name, str(value))

        if attempt_eval:
            try:
                self.value = int(eval(op))
            except NameError:
                self.value = f'({op})'
        else:
            if '=' not in op:
                self.value = f'({op})'
            else:
                self.value = op
        return True


class MonkeyYellingDag:

    def __init__(self, inputs, always_attempt_eval=True) -> None:
        self.monkeys = {}
        self.always_attempt_eval = always_attempt_eval
        for line in inputs:
            name, op = line.split(': ')
            matches = re.findall('[a-z]{4}', op)
            self.monkeys[name] = Monkey(name=name, operation=op, dependencies=set(matches))

    def run_dag_step(self):
        monkeys_ran = 0
        for m in self.monkeys.values():
            if m.value is not None:
                continue

            monkeys_ran += m.run_operation(
                {d: self.monkeys[d].value for d in m.dependencies if self.monkeys[d].value is not None},
                attempt_eval=self.always_attempt_eval or m.name != 'root'
            )

        return monkeys_ran

    def run_dag(self):
        monkeys_ran = 1
        while monkeys_ran > 0:
            monkeys_ran = self.run_dag_step()
            print(f'Ran {monkeys_ran} monkeys')

    def fetch_dependencies(self, monkey):
        dependencies = {}
        for d in monkey.dependencies:
            if self.monkeys[d].value is None:
                return None
            dependencies[d] = self.monkeys[d].value
        return dependencies


class Day21(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        dag = MonkeyYellingDag(inputs=inputs)
        dag.run_dag()
        return dag.monkeys['root'].value

    def part_2(self, inputs: List[str]):
        dag = MonkeyYellingDag(inputs=inputs, always_attempt_eval=False)
        dag.monkeys['humn'].value = 'HUMAN'
        dag.monkeys['root'].operation = dag.monkeys['root'].operation.replace('+', '=')
        dag.run_dag()
        left, right = dag.monkeys['root'].value.split(' = ')
        human = symbols('HUMAN')
        solutions = solve(Eq(parse_expr(left), parse_expr(right)), human, dict=True)
        return solutions[0][human]
