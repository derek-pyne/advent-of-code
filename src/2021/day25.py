import time
from enum import Enum
import pandas as pd

import warnings

warnings.simplefilter(action='ignore',
                      category=FutureWarning)  # setting ignore as a parameter and further adding category


LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

class SeaCucumbers:
    class Cucumber(Enum):
        EMPTY = '.'
        EAST = '>'
        SOUTH = 'v'

    def __init__(self, f_path: str) -> None:
        sea_floor_lists = []
        with open(f_path) as f:
            for line in f:
                # parsed_line = [self.Cucumber(c) for c in line.strip()]
                parsed_line = [c for c in line.strip()]
                sea_floor_lists.append(parsed_line)

        self.sea_floor = pd.DataFrame(sea_floor_lists)

        self.check_statuses()
        self.display_sea_floor()

    def check_statuses(self):
        self.check_occupied()
        self.check_east_occupied()
        self.check_south_occupied()

        self.check_east_movement()
        self.check_south_movement()

    def display_sea_floor(self):
        for i in range(10):
            print(LINE_UP, end=LINE_CLEAR)
        print(self.sea_floor)
        time.sleep(.5)
        # print('>> Sea floor <<')
        # print(self.sea_floor)
        # print('>> Occupied <<')
        # print(self.occupied)

    def check_occupied(self):
        self.occupied = self.sea_floor != '.'

    def check_east_occupied(self):
        self.east_occupied = self.sea_floor == '>'

    def check_south_occupied(self):
        self.south_occupied = self.sea_floor == 'v'

    def check_east_movement(self):
        self.east_movement = self.occupied.shift(-1, axis=1)
        self.east_movement.iloc[:, -1] = self.occupied.iloc[:, 0]
        self.east_movement = self.east_movement.astype(bool)
        self.east_movement = ~self.east_movement

    def check_south_movement(self):
        self.south_movement = self.occupied.shift(-1)
        self.south_movement.iloc[-1, :] = self.occupied.iloc[0, :]
        self.south_movement = self.south_movement.astype(bool)
        self.south_movement = ~self.south_movement

    def move_east(self):
        self.check_statuses()
        able_to_move = self.east_occupied & self.east_movement
        unable_to_move = able_to_move ^ self.east_occupied

        moved_east = able_to_move.shift(1, axis=1)
        moved_east.iloc[:, 0] = able_to_move.iloc[:, -1]
        moved_east = moved_east.astype(bool)

        final_east = moved_east | unable_to_move

        # Remove current east cucumbers
        self.sea_floor[self.east_occupied] = '.'

        # Replace with new east cucumbers
        self.sea_floor[final_east] = '>'

    def move_south(self):
        self.check_statuses()
        able_to_move = self.south_occupied & self.south_movement
        unable_to_move = able_to_move ^ self.south_occupied

        moved_south = able_to_move.shift(1)
        moved_south.iloc[0, :] = able_to_move.iloc[-1, :]
        moved_south = moved_south.astype(bool)

        final_south = moved_south | unable_to_move

        # Remove current east cucumbers
        self.sea_floor[self.south_occupied] = '.'

        # Replace with new east cucumbers
        self.sea_floor[final_south] = 'v'

    def run_sim(self):
        i = 0

        while True:
            current_sea_floor = self.sea_floor.copy()
            i += 1
            # print(f'>> {i}')
            self.move_east()
            self.move_south()

            self.display_sea_floor()
            
            if self.sea_floor.equals(current_sea_floor):
                return


sc = SeaCucumbers('day25_easy.txt')
# sc.move_east()
# sc.display_sea_floor()
# sc.move_south()
# sc.display_sea_floor()
sc.run_sim()
