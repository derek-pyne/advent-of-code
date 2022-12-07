from dataclasses import dataclass, field
from typing import List, Dict

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class File:
    name: str
    size: int
    parent: None = field(repr=False)

    def pretty_print(self, indent=0):
        print(f'{" " * indent}- {self.name} (file, size={self.size})')


@dataclass
class Directory:
    name: str
    parent: None
    dirs: Dict = field(default_factory=dict, repr=False)
    files: Dict = field(default_factory=dict, repr=False)

    def add_dir(self, d: 'Directory'):
        self.dirs[d.name] = d

    def add_file(self, f: File):
        self.files[f.name] = f

    @property
    def size(self):
        return sum([f.size for f in self.files.values()]) + sum([d.size for d in self.dirs.values()])

    def pretty_print(self, indent=0):
        print(f'{" " * indent}- {self.name} (dir, size={self.size})')
        for d in self.dirs.values():
            d.pretty_print(indent=indent + 2)
        for f in self.files.values():
            f.pretty_print(indent=indent + 2)

    def all_nested_dirs(self):
        nested_dirs = list(self.dirs.values())

        for d in self.dirs.values():
            nested_dirs.extend(d.all_nested_dirs())

        return nested_dirs


@dataclass
class Command:
    command: str
    outputs: List[str] = field(default_factory=list)


class Day7(AdventOfCodePuzzle):
    @staticmethod
    def follow_commands(commands, pretty_print=True):
        # Initializing filesystem with just root dir
        root = Directory('/', parent=None)
        current_dir = root
        for c in commands:
            if c.command == 'ls':
                for output in c.outputs:
                    if output.startswith('dir'):
                        dir_name = output.split()[1]
                        if dir_name not in current_dir.dirs:
                            current_dir.add_dir(Directory(name=dir_name, parent=current_dir))
                    else:
                        file_size, f_name = output.split()
                        if f_name not in current_dir.files:
                            current_dir.add_file(File(
                                name=f_name,
                                size=int(file_size),
                                parent=current_dir
                            ))
            elif c.command.startswith('cd'):
                target = c.command.split()[1]
                if target == '/':
                    current_dir = root
                elif target == '..':
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.dirs[target]
        if pretty_print:
            print()
            root.pretty_print()
        return root

    @staticmethod
    def parse_commands(inputs):
        commands = []
        current_command = None
        for line in inputs[1:]:
            if line.startswith('$'):
                current_command = Command(command=line[2:])
                commands.append(current_command)
            else:
                current_command.outputs.append(line)
        return commands

    def part_1(self, inputs: List[str]):
        commands = self.parse_commands(inputs)
        root = self.follow_commands(commands, pretty_print=True)
        all_dirs = root.all_nested_dirs()
        return sum([d.size for d in all_dirs if d.size < 100000])

    def part_2(self, inputs: List[str]):
        commands = self.parse_commands(inputs)
        root = self.follow_commands(commands, pretty_print=True)
        all_dirs = root.all_nested_dirs()

        total_disk_size = 70000000
        unused_size = total_disk_size - root.size
        space_needed = 30000000 - unused_size
        return min([d for d in all_dirs if d.size >= space_needed], key=lambda x: x.size).size
