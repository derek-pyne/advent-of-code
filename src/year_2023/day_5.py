import os
from dataclasses import dataclass, field


@dataclass
class Mapping:
    dest: int
    source: int
    range: int
    
    @property
    def source_end(self) -> int:
        return self.source+self.range
    
@dataclass
class ValueRange:
    start: int
    count: int
    
    @property
    def end(self):
        return self.start + self.count-1


@dataclass
class AlmanacMapping:
    source: str
    dest: str
    mappings: list[Mapping] = field(default_factory=list)
    
    def next(self, x: int) -> int:
        for m in self.mappings:
            if m.source <= x <= m.source + m.range:
                return m.dest + (x - m.source)
        return x
    
    def next_range(self, input_ranges: list[ValueRange]) -> list[ValueRange]:
        ranges_to_return = []
        for vr in input_ranges:
            matches_mapping = False
            for m in self.mappings:
                if m.source <= vr.start <= m.source_end:
                    # Checking if it can hold the entire range
                    if vr.end <= m.source_end:
                        new_vr = ValueRange(start=m.dest + (vr.start - m.source), count=vr.count)
                        ranges_to_return.append(new_vr)
                    else:
                        # How much can we hold
                        leftovers =  vr.end - m.source_end
                        
                        # Leftover range
                        new_vr = ValueRange(start=m.dest+(vr.start-m.source), count=vr.count-leftovers)
                        ranges_to_return.append(new_vr)
                        
                        leftover_range = ValueRange(start=vr.start+(vr.count-leftovers), count=leftovers)
                        ranges_to_return.extend(self.next_range([leftover_range]))
                    matches_mapping = True
                    break
            if not matches_mapping:
                ranges_to_return.append(vr)
        return ranges_to_return
            

with open(os.path.join(os.path.dirname(__file__), 'inputs/day_5.txt')) as f:
    sections = f.read().split('\n\n')
seeds = [int(x) for x in sections[0].split('seeds: ')[1].split(' ')]

maps = {}
for s in sections[1:]:
    splits = s.split('\n')
    source, dest = splits[0].split(' ')[0].split('-to-')
    am = AlmanacMapping(source=source, dest=dest)
    for num_split in splits[1:]:
        nums = num_split.split()
        if len(nums) != 3:
            continue
        am.mappings.append(Mapping(*[int(x) for x in nums]))
    maps[am.source] = am
        


def calculate_location_from_seed(seed, range_mode=False):
    num = seed
    current = 'seed'
    while current != 'location':
        current_map = maps[current]
        if range_mode:
            num = current_map.next_range(num)
        else:
            num = current_map.next(num)
        current = current_map.dest
    return num

locations = [calculate_location_from_seed(seed) for seed in seeds]
print(f'Part 1: {min(locations)}')


ranges = []
for i in range(0, len(seeds), 2):
    ranges.extend(calculate_location_from_seed([ValueRange(seeds[i], seeds[i+1])], range_mode=True))

print(ranges)
print(f'Part 2: {min([r.start for r in ranges])}')
print(37806486)
