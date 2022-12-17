import re
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Sensor:

    def __init__(self, raw_input: str) -> None:
        match = re.match(
            'Sensor at x=([-\d]*), y=([-\d]*): closest beacon is at x=([-\d]*), y=([-\d]*)',
            raw_input
        )
        self.sensor_x = int(match.groups()[0])
        self.sensor_y = int(match.groups()[1])
        self.beacon_x = int(match.groups()[2])
        self.beacon_y = int(match.groups()[3])
        self.manhattan_distance = abs(self.beacon_x - self.sensor_x) + abs(self.beacon_y - self.sensor_y)

    def __repr__(self) -> str:
        return f'Sensor(d: {self.manhattan_distance}, sensor:({self.sensor_x},{self.sensor_y}), beacon:({self.beacon_x},{self.beacon_y})'


class SensorGrid:

    def __init__(self, raw_input) -> None:
        self.sensors = [Sensor(line) for line in raw_input]

    def counts_along_row(self, y):
        x_with_beacon = set()
        x_with_sensor = set()
        x_without_beacon = set()

        for s in self.sensors:
            left_right_manhattan = s.manhattan_distance - abs(y - s.sensor_y)
            if left_right_manhattan >= 0:
                for i in range(-left_right_manhattan, left_right_manhattan + 1):
                    x = s.sensor_x + i
                    if x not in x_without_beacon:
                        x_without_beacon.add(x)

        for s in self.sensors:
            if s.sensor_y == y:
                if s.sensor_x in x_without_beacon:
                    x_without_beacon.remove(s.sensor_x)
                if s.sensor_x not in x_with_sensor:
                    x_with_sensor.add(s.sensor_x)
            if s.beacon_y == y:
                if s.beacon_x in x_without_beacon:
                    x_without_beacon.remove(s.beacon_x)
                if s.beacon_x not in x_with_beacon:
                    x_with_beacon.add(s.beacon_x)

        return dict(
            beacon=len(x_with_beacon),
            sensor=len(x_with_sensor),
            no_beacon=len(x_without_beacon)
        )

    def search_for_possible_spot(self, grid_max, man_offset=1):
        for s in self.sensors:
            for y_offset, width in enumerate(range((s.manhattan_distance + man_offset) * 2 + 1, 0, -2)):
                x = s.sensor_x - (width // 2)
                y = s.sensor_y - y_offset
                if self.check_point_is_outside_sensors(x, y, grid_max):
                    return x, y
                x = s.sensor_x + (width // 2)
                y = s.sensor_y - y_offset
                if self.check_point_is_outside_sensors(x, y, grid_max):
                    return x, y
                x = s.sensor_x - (width // 2)
                y = s.sensor_y + y_offset
                if self.check_point_is_outside_sensors(x, y, grid_max):
                    return x, y
                x = s.sensor_x + (width // 2)
                y = s.sensor_y + y_offset
                if self.check_point_is_outside_sensors(x, y, grid_max):
                    return x, y
        return None

    def check_point_is_outside_sensors(self, p_x, p_y, grid_max) -> bool:
        for s in self.sensors:
            # Checking if point sitting on beacon or sensor
            if (s.beacon_x == p_x and s.beacon_y == p_y) or (s.sensor_x == p_x and s.sensor_y == p_y):
                return False
            elif (abs(p_x - s.sensor_x) + abs(p_y - s.sensor_y)) <= s.manhattan_distance:
                return False
            elif (p_x < 0) or (p_y < 0) or (p_x > grid_max) or (p_y > grid_max):
                return False
        return True


class Day15(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        sg = SensorGrid(inputs)

        y = 10 if len(inputs) < 15 else 2000000
        counts = sg.counts_along_row(y)
        return counts['no_beacon']

    def part_2(self, inputs: List[str]):
        # For each sensor, build the possible options by looking at the places that are a
        # single manhattan distance greater than each sensor
        # Eliminate the places within the bounds
        # Since there is only one possible point, this should find the answer with an offset of just 1

        sg = SensorGrid(inputs)

        grid_max = 20 if len(inputs) < 15 else 4E6

        x, y = sg.search_for_possible_spot(grid_max)
        return int((x * 4E6) + y)
