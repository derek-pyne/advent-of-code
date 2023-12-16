import os
from dataclasses import dataclass, field

with open(os.path.join(os.path.dirname(__file__), 'inputs/day_5.txt')) as f:
    sections = f.read().split('\n\n')
seeds = sections[0].split('seeds: ')[1].split(' ')


@dataclass
class AlmanacMapping:
    source: str
    dest: str
    data: list = field(default_factory=list)

maps = []
for s in sections[1:]:
    splits = s.split('\n')
    source, dest = splits[0].split(' ')[0].split('-to-')
    am = AlmanacMapping(source=source, dest=dest)
    for num_split in splits[1:]:
        am.data.append(num_split.split())
    maps.append(am)
        
print(maps)
