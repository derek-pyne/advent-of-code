from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


class Game:
    def __init__(self, me_input: str, opponent_input: str):
        self.me = self.convert_input(me_input)
        self.opponent = self.convert_input(opponent_input)
        self.score = self.outcome_score + self.input_score

    def convert_input(self, raw_input: str) -> str:
        if raw_input in ['A', 'X']:
            return 'rock'
        elif raw_input in ['B', 'Y']:
            return 'paper'
        elif raw_input in ['C', 'Z']:
            return 'scissors'
        else:
            raise ValueError(f'Bad raw_input to convert: {raw_input}')

    @property
    def outcome_score(self) -> int:
        if self.me == self.opponent:
            # Draw
            return 3

        winning_outcomes = {
            'rock':     'paper',
            'paper':    'scissors',
            'scissors': 'rock',
        }
        if self.me == winning_outcomes[self.opponent]:
            # Win
            return 6
        else:
            # Lose
            return 0

    @property
    def input_score(self) -> int:
        if self.me == 'rock':
            return 1
        elif self.me == 'paper':
            return 2
        elif self.me == 'scissors':
            return 3
        else:
            raise ValueError


class GameSecret(Game):
    def __init__(self, opponent_input: str, desired_outcome_input):
        super().__init__(me_input='X', opponent_input=opponent_input)
        self.desired_outcome = self.convert_desired_outcome_input(desired_outcome_input)
        self.me = self.what_i_should_play()
        self.score = self.outcome_score + self.input_score

    def convert_desired_outcome_input(self, raw_input: str) -> str:
        if raw_input == 'X':
            return 'lose'
        elif raw_input == 'Y':
            return 'draw'
        elif raw_input == 'Z':
            return 'win'
        else:
            raise ValueError(f'Bad desired_outcome_input: {raw_input}')

    def what_i_should_play(self):
        if self.desired_outcome == 'draw':
            return self.opponent

        winning_outcomes = {
            'rock':     'paper',
            'paper':    'scissors',
            'scissors': 'rock',
        }
        losing_outcomes = {v: k for k, v in winning_outcomes.items()}
        if self.desired_outcome == 'win':
            return winning_outcomes[self.opponent]
        else:
            return losing_outcomes[self.opponent]


def get_games(inputs: List[str]) -> List[Game]:
    games = []
    for line in inputs:
        split_line = line.strip().split(' ')
        games.append(Game(
            opponent_input=split_line[0],
            me_input=split_line[1],
        ))
    return games


def get_secret_games(inputs: List[str]) -> List[GameSecret]:
    secret_games = []
    for line in inputs:
        split_line = line.strip().split(' ')
        secret_games.append(GameSecret(
            opponent_input=split_line[0],
            desired_outcome_input=split_line[1],
        ))
    return secret_games


class Day2(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]) -> int:
        games = get_games(inputs=inputs)
        return sum([game.score for game in games])

    def part_2(self, inputs: List[str]) -> int:
        secret_games = get_secret_games(inputs=inputs)
        return sum([game.score for game in secret_games])
