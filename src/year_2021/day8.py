from collections import Counter
from typing import List

from src.advent_of_code_puzzle import AdventOfCodePuzzle


def unique_numbers(ten_digit_section):
    # Maps len of segments to the unique number it must be
    unique_number_len = {
        2: 1,
        3: 7,
        4: 4,
        7: 8,
    }

    decoder = {}
    for x in ten_digit_section:
        if len(x) in unique_number_len:
            decoder[''.join(sorted(x))] = unique_number_len[len(x)]
    return decoder


def decode_with_unique_numbers(decoder, output):
    decoded = ''
    for x in output:
        decoded += str(decoder.get(''.join(sorted(x)), ''))
    return decoded


d = {
    'abcefg':  0,
    'cf':      1,
    'acdeg':   2,
    'acdfg':   3,
    'bcdf':    4,
    'abdfg':   5,
    'abdefg':  6,
    'acf':     7,
    'abcdefg': 8,
    'abcdfg':  9,
}


def deduce_segments(decoder, ten_digit_section):
    decoder_inv = {v: k for k, v in decoder.items()}
    position_mapping = {}
    num_to_segments = {v: k for k, v in decoder.items()}

    # A position is the difference between 7 and 1
    position_mapping['a'] = list(set(num_to_segments[7]) - set(num_to_segments[1]))[0]

    segment_counts_across_all = Counter([x for k in d.keys() for x in k])
    segment_counts_across_all_inv = {v: k for k, v in segment_counts_across_all.items()}

    segment_counts = Counter([x for k in ten_digit_section for x in k])
    segment_counts_inv = {v: k for k, v in segment_counts.items()}

    # e is the only digit with 4 occurrences in the ten digit sequence
    position_mapping[segment_counts_across_all_inv[4]] = segment_counts_inv[4]

    # f is the only digit with 9 occurrences in the ten digit sequence
    position_mapping[segment_counts_across_all_inv[9]] = segment_counts_inv[9]

    # b is the only digit with 6 occurrences in the ten digit sequence
    position_mapping[segment_counts_across_all_inv[6]] = segment_counts_inv[6]

    # can now deduce c now that we have f and the 1 digit
    position_mapping['c'] = list(set(decoder_inv[1]) - set(position_mapping['f']))[0]

    # Can now deduce d using the 4 digit with bcf
    position_mapping['d'] = list(
        set(decoder_inv[4]) - {position_mapping['b'], position_mapping['c'], position_mapping['f']}
    )[0]

    # Can now get final digit using elimination
    position_mapping['g'] = list(set('abcdefg') - set(position_mapping.values()))[0]

    return {v: k for k, v in position_mapping.items()}


def decode_from_segments(segment_mapping, output):
    decoded_output = ''
    for x in output:
        decoded_segments = [segment_mapping[i] for i in x]
        decoded_output += str(d[''.join(sorted(decoded_segments))])
    return int(decoded_output)


def parse_input(inputs):
    signals = []

    for x in inputs:
        ten_digit_section, output = x.split(' | ')
        ten_digit_section = ten_digit_section.split()
        output = output.split()
        signals.append((ten_digit_section, output))
    return signals


class Day8(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        signals = parse_input(inputs)

        decoded_outputs = []
        for ten_digit_section, output in signals:
            unique_number_decoder = unique_numbers(ten_digit_section)
            decoded_output = decode_with_unique_numbers(unique_number_decoder, output)
            decoded_outputs.append(decoded_output)

        return sum([len(x) for x in decoded_outputs])

    def part_2(self, inputs: List[str]):
        signals = parse_input(inputs)

        decoded_outputs = []
        for ten_digit_section, output in signals:
            unique_number_decoder = unique_numbers(ten_digit_section)
            segment_mapping = deduce_segments(unique_number_decoder, ten_digit_section)
            decoded_output = decode_from_segments(segment_mapping, output)
            decoded_outputs.append(decoded_output)

        return sum(decoded_outputs)
