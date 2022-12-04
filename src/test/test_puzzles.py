import importlib
import os
from typing import List

import pytest


def read_input(f_name: str, year: int) -> List[str]:
    inputs_folder = os.path.join(os.path.dirname(__file__), f'../year_{year}/inputs')
    f_path = os.path.join(inputs_folder, f_name)
    with open(f_path) as f:
        return [line.strip() for line in f.readlines()]


@pytest.fixture
def input_example(day, year):
    return read_input(f'day{day}_example.txt', year)


@pytest.fixture
def input_test(day, year):
    return read_input(f'day{day}.txt', year)


@pytest.mark.parametrize(
    "year,day,expected_example_1,expected_test_1,expected_example_2,expected_test_2",
    [
        (2022, 1, 24000, 69528, 45000, 206152),
        (2022, 2, 15, 17189, 12, 13490),
        (2022, 3, 157, 7568, 70, 2780),
        (2022, 4, 2, 526, 4, 886),
        (2021, 3, 198, 2250414, 230, 6085575),
    ]
)
@pytest.mark.usefixtures()
class TestDay:

    def test_part_1_example(
            self, year, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_example
    ):
        output = solver.part_1(inputs=input_example)
        assert output == expected_example_1

    def test_part_1_test(
            self, year, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_test
    ):
        output = solver.part_1(inputs=input_test)
        assert output == expected_test_1

    def test_part_2_example(
            self, year, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_example
    ):
        output = solver.part_2(inputs=input_example)
        assert output == expected_example_2

    def test_part_2_test(
            self, year, day, expected_example_1, expected_test_1, expected_example_2, expected_test_2,
            solver, input_test
    ):
        output = solver.part_2(inputs=input_test)
        assert output == expected_test_2


@pytest.fixture
def solver(day, year):
    day_module = importlib.import_module(f'src.year_{year}.day{day}')
    return getattr(day_module, f'Day{day}')()