import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Num:
    value_str: str = ''
    locations: set = field(default_factory=set)
    is_valid: bool = False
    
    @property
    def value(self):
        return int(self.value_str)
    
    def add_digit(self, c, x, y):
        self.locations.add((x, y))
        self.value_str += c
        
    def check_validity(self, valid_locations: set):
        for loc in self.locations:
            if loc in valid_locations:
                self.is_valid = True
                return
        self.is_valid = False
        
@dataclass
class Gear:
    location: tuple
    part_numbers: list[int] = field(default_factory=list)
    
    @property
    def adjacent_locations(self) -> set:
        locs = set()
        for x_val in [self.location[0] - 1, self.location[0], self.location[0] + 1]:
            for y_val in [self.location[1] - 1, self.location[1], self.location[1] + 1]:
                locs.add((x_val, y_val))
        return locs
    def check_validity(self, nums: List[Num]):
        for n in nums:
            if len(self.adjacent_locations.intersection(n.locations)) > 0:
                self.part_numbers.append(n.value)
                
    @property
    def gear_ratio(self) -> int:
        return 0 if len(self.part_numbers) != 2 else self.part_numbers[0] * self.part_numbers[1]


valid_locations = set()
nums = []
gears = []

with open(os.path.join(os.path.dirname(__file__), 'inputs/day_3.txt')) as f:
    y = 0
    for line in f.readlines():
        current_num = None
        x = 0
        for c in line.strip():
            if c == '.':
                if current_num is not None:
                    current_num = None
            elif c in '1234567890':
                if current_num is None:
                    current_num = Num()
                    nums.append(current_num)
                current_num.add_digit(c, x, y)
            else:
                if current_num is not None:
                    current_num = None
                for x_val in [x-1, x, x+1]:
                    for y_val in [y-1, y, y+1]:
                        valid_locations.add((x_val, y_val))
                if c == '*':
                    gears.append(Gear((x, y)))
            x += 1
        y += 1
    
# Part 1
for num in nums:
    num.check_validity(valid_locations)
print(f'Sum is: {sum([n.value for n in nums if n.is_valid])}')

# Part 2
for g in gears:
    g.check_validity(nums)
print(f'Gear ratio sum: {sum([g.gear_ratio for g in gears])}')
