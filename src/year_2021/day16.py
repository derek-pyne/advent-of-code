from dataclasses import dataclass, field
from typing import List, Tuple

from src.advent_of_code_puzzle import AdventOfCodePuzzle


@dataclass
class Packet:
    version: int
    type_id: int
    value: int = None
    total_bit_length: int = None
    num_subpackets: int = None
    subpackets: List['Packet'] = field(default_factory=list, repr=False)

    def value_str(self):
        if self.value is not None:
            return str(self.value)
        elif self.type_id == 0:
            return f' ({" + ".join([p.value_str() for p in self.subpackets])}) '
        elif self.type_id == 1:
            return f' ({" * ".join([p.value_str() for p in self.subpackets])}) '
        elif self.type_id == 2:
            return f' min([{", ".join([p.value_str() for p in self.subpackets])}]) '
        elif self.type_id == 3:
            return f' max([{", ".join([p.value_str() for p in self.subpackets])}]) '
        elif self.type_id == 5:
            return f' (({self.subpackets[0].value_str()}) > ({self.subpackets[1].value_str()})) '
        elif self.type_id == 6:
            return f' (({self.subpackets[0].value_str()}) < ({self.subpackets[1].value_str()})) '
        elif self.type_id == 7:
            return f' (({self.subpackets[0].value_str()}) == ({self.subpackets[1].value_str()})) '


class PacketDecoder:

    def __init__(self, inputs) -> None:
        data = ''
        for c in inputs[0]:
            data += '{0:04b}'.format(int(c, 16))
        self.data = data
        self.root_packet = None

    def parse_packets(self):
        _, self.root_packet = self.parse(self.data)

    def parse(self, data) -> Tuple[str, 'Packet']:
        version, data = self.pop_from_string(data, 3)
        version = int(version, 2)
        type_id, data = self.pop_from_string(data, 3)
        type_id = int(type_id, 2)

        # Literal value packet
        if type_id == 4:
            lit_value = ''
            while True:
                group, data = self.pop_from_string(data, 5)
                lit_value += group[1:]
                if group[0] == '0':
                    break
            lit_value = int(lit_value, 2)
            packet = Packet(version=version, type_id=type_id, value=lit_value)
            return data, packet
        # Operator packet
        else:
            length_type_id, data = self.pop_from_string(data, 1)
            if length_type_id == '0':
                total_bit_length, data = self.pop_from_string(data, 15)
                total_bit_length = int(total_bit_length, 2)
                p = Packet(version=version, type_id=type_id, total_bit_length=total_bit_length)
                operator_data, data = self.pop_from_string(data, total_bit_length)
                while operator_data:
                    operator_data, subpacket = self.parse(operator_data)
                    p.subpackets.append(subpacket)
                return data, p
            else:
                num_subpackets, data = self.pop_from_string(data, 11)
                num_subpackets = int(num_subpackets, 2)
                p = Packet(version=version, type_id=type_id, num_subpackets=num_subpackets)
                for i in range(num_subpackets):
                    data, subpacket = self.parse(data)
                    p.subpackets.append(subpacket)
                return data, p

    @staticmethod
    def pop_from_string(s, n):
        return s[:n], s[n:]

    def version_sum_from_root(self):
        return self.version_sum(0, self.root_packet)

    def version_sum(self, version_sum, packet):
        return packet.version + version_sum + sum([self.version_sum(0, p) for p in packet.subpackets])


class Day16(AdventOfCodePuzzle):
    def part_1(self, inputs: List[str]):
        decoder = PacketDecoder(inputs)
        decoder.parse_packets()
        return decoder.version_sum_from_root()

    def part_2(self, inputs: List[str]):
        decoder = PacketDecoder(inputs)
        decoder.parse_packets()
        decoded_expression = decoder.root_packet.value_str()
        return int(eval(decoded_expression))
