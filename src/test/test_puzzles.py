import importlib
import os
from typing import List

import pytest


def read_input(f_name: str, year: int, strip_lines=True) -> List[str]:
    inputs_folder = os.path.join(os.path.dirname(__file__), f'../year_{year}/inputs')
    f_path = os.path.join(inputs_folder, f_name)
    with open(f_path) as f:
        return [line.strip() if strip_lines else line for line in f.readlines()]


@pytest.fixture
def input_example(day, year, solver):
    return read_input(f'day{day}_example.txt', year, strip_lines=solver.strip_input_lines)


@pytest.fixture
def input_test(day, year, solver):
    return read_input(f'day{day}.txt', year, strip_lines=solver.strip_input_lines)


@pytest.mark.parametrize(
    "year,day,expected_example_1,expected_test_1,expected_example_2,expected_test_2",
    [
        # 2022
        # (2022, 1, 24000, 69528, 45000, 206152),
        # (2022, 2, 15, 17189, 12, 13490),
        # (2022, 3, 157, 7568, 70, 2780),
        # (2022, 4, 2, 526, 4, 886),
        # (2022, 5, 'CMZ', 'CWMTGHBDW', 'MCD', 'SSCGWJCRB'),
        # (2022, 6, 11, 1647, 26, 2447),
        (2022, 7, 95437, 1307902, 24933642, 7068748),

        # # 2021
        # (2021, 1, 7, 1502, 5, 1538),
        # (2021, 2, 150, 1989014, 900, 2006917119),
        # (2021, 3, 198, 2250414, 230, 6085575),
        # (2021, 4, 4512, 49860, 1924, 24628),
        # (2021, 5, 5, 6666, 12, 19081),
        # (2021, 6, 5934, 350605, 26984457539, 1592778185024),
        # (2021, 7, 37, 344535, 168, 95581659),
        # (2021, 8, 26, 375, 61229, 1019355),
        # (2021, 9, 15, 494, 1134, 1048128),
        # (2021, 10, 26397, 319329, 288957, 3515583998),
        # (2021, 25, 58, 353, 1, 1),
        # 
        # # 2020
        # (2020, 1, 514579, 211899, 241861950, 275765682),
        # 
        # # 2015
        # (2015, 1, -1, 232, 5, 1783),
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
