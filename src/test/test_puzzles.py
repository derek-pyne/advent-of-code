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
        # (2022, 7, 95437, 1307902, 24933642, 7068748),
        # (2022, 8, 21, 1798, 8, 259308),
        # (2022, 9, 13, 6464, 1, 2604),
        # (2022, 10, 13140, 17380, 1, 1),
        # (2022, 11, 10605, 50830, 2713310158, 14399640002),
        # (2022, 12, 31, 352, 29, 345),
        # (2022, 13, 13, 5340, 140, 21276),
        # (2022, 14, 24, 805, 93, 25161),
        # (2022, 15, 26, 4665948, 56000011, 13543690671045),
        # (2022, 16, 1651, 1789, 1707, 2496),
        # (2022, 17, 3068, 3059, 1514285714288, 1500874635587),
        # (2022, 18, 64, 4628, 58, 2582),
        # (2022, 19, 33, 1365, 3472, 4864),
        # (2022, 20, 3, 19559, 1623178306, 912226207972),
        # (2022, 21, 152, 170237589447588, 301, 3712643961892),
        # (2022, 22, 6032, 186128, 5031, 34426),
        # (2022, 23, 110, 4123, 20, 1029),
        # (2022, 24, 18, 249, 54, 735),
        # (2022, 25, '2=-1=0', '2==0=0===02--210---1', 1, 1),

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
        # (2021, 11, 1656, 1793, 195, 247),
        # (2021, 12, 226, 4167, 3509, 98441),
        # (2021, 13, 17, 638, 'CJCKBAPB', 'CJCKBAPB'),
        # (2021, 14, 1588, 2967, 2188189693529, 3692219987038),
        # (2021, 15, 40, 390, 315, 2814),
        # (2021, 16, 11, 967, 9, 12883091136209),
        # (2021, 17, 45, 10296, 112, 2371),
        # (2021, 25, 58, 353, 1, 1),
        # 
        # # 2020
        # (2020, 1, 514579, 211899, 241861950, 275765682),
        # 
        # 2019
        # (2019, 1, 34241, 3495189, 51316, 5239910),
        (2019, 2, 2782414, 2782414, 9820, 9820),
        (2019, 5, 4601506, 4601506, 5525561, 5525561),
        (2019, 9, 2406950601, 2406950601, 83239, 83239),
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
