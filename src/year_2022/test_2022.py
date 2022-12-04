import importlib
import os
from typing import List

import pytest

INPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'inputs')


def read_input(f_name: str) -> List[str]:
    f_path = os.path.join(INPUT_FOLDER, f_name)
    with open(f_path) as f:
        return [line.strip() for line in f.readlines()]


@pytest.fixture
def input_example(day):
    return read_input(f'day{day}_example.txt')


@pytest.fixture
def input_test(day):
    return read_input(f'day{day}.txt')


@pytest.fixture
def solver(day):
    day_module = importlib.import_module(f'src.year_2022.day{day}')
    return getattr(day_module, f'Day{day}')()


@pytest.mark.parametrize(
    "day,expected_example_1,expected_test_1,expected_example_2,expected_test_2",
    [
        (1, 24000, 69528, 45000, 206152),
        (2, 15, 17189, 12, 13490),
        (3, 157, 7568, 70, 2780),
        (4, 2, 526, 4, 886),
    ]
)
@pytest.mark.usefixtures()
class TestDay:

    def test_part_1_example(
            self, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_example
    ):
        output = solver.part_1(inputs=input_example)
        assert output == expected_example_1

    def test_part_1_test(
            self, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_test
    ):
        output = solver.part_1(inputs=input_test)
        assert output == expected_test_1

    def test_part_2_example(
            self, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_example
    ):
        output = solver.part_2(inputs=input_example)
        assert output == expected_example_2

    def test_part_2_test(
            self, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_test
    ):
        output = solver.part_2(inputs=input_test)
        assert output == expected_test_2
