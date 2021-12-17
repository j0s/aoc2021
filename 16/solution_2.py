#!/bin/env python

from typing import Tuple, List, ClassVar, Type, Any
import sys
from os.path import exists
from functools import reduce


def ascii_to_binary(ascii: str) -> str:
    """
    >>> ascii_to_binary('a')
    '1010'
    >>> ascii_to_binary('1')
    '0001'
    >>> ascii_to_binary('0b')
    '00001011'
    """
    return ''.join([f'{int(char, 16):04b}' for char in ascii])


def binary_to_int(bin: str) -> int:
    return int(bin, 2)


def parse_int(input: str, len: int) -> Tuple[str, int]:
    return input[len:], binary_to_int(input[:len])


class Packet(object):
    typ: ClassVar[int] = -1

    def __init__(self, ver: int):
        self.ver = ver

    def ver_sum(self) -> int:
        return self.ver

    def value(self) -> int:
        raise Exception('can\'t call value on base class')

    @classmethod
    def parse(cls, ver: int, data: str) -> Tuple[str, Any]:
        raise Exception('can\'t parse Packet')


class ParentPacket(Packet):
    def __init__(self, ver):
        super().__init__(ver)
        self.sub_pkts: List[Packet] = []

    def __repr__(self) -> str:
        sub_pkts_str = '['
        for pkt in self.sub_pkts:
            for line in pkt.__repr__().split('\n'):
                sub_pkts_str += '\n  ' + line
        sub_pkts_str += '\n]'
        return f'{self.__class__.__name__} (v: {self.ver}) {sub_pkts_str}'

    def ver_sum(self) -> int:
        return self.ver + sum([p.ver_sum() for p in self.sub_pkts])

    @classmethod
    def parse(cls, ver: int, data: str) -> Tuple[str, Packet]:
        p = cls(ver)
        data, len_type_id = parse_int(data, 1)
        if len_type_id == 0:
            data, sub_pkt_len = parse_int(data, 15)
            p.sub_pkts = parse_packets(data[:sub_pkt_len])
            data = data[sub_pkt_len:]
        elif len_type_id == 1:
            data, num_sub_pkts = parse_int(data, 11)
            for n in range(num_sub_pkts):
                data, pkt = parse_packet(data)
                p.sub_pkts.append(pkt)
        return data, p


class SumPacket(ParentPacket):
    typ: ClassVar[int] = 0

    def __init__(self, ver):
        super().__init__(ver)

    def value(self) -> int:
        return sum([p.value() for p in self.sub_pkts])


class ProductPacket(ParentPacket):
    typ: ClassVar[int] = 1

    def __init__(self, ver):
        super().__init__(ver)

    def value(self) -> int:
        return reduce(lambda x, y: x * y, [p.value() for p in self.sub_pkts])


class MinPacket(ParentPacket):
    typ: ClassVar[int] = 2

    def __init__(self, ver):
        super().__init__(ver)

    def value(self) -> int:
        return min([p.value() for p in self.sub_pkts])


class MaxPacket(ParentPacket):
    typ: ClassVar[int] = 3

    def __init__(self, ver):
        super().__init__(ver)

    def value(self) -> int:
        return max([p.value() for p in self.sub_pkts])


class LiteralPacket(Packet):
    typ: ClassVar[int] = 4

    def __init__(self, ver, val):
        super().__init__(ver)
        self.val = val

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (v: {self.ver}, val: {self.val})'

    def value(self) -> int:
        return self.val

    @classmethod
    def parse(cls, ver: int, input: str) -> Tuple[str, Any]:
        """
        >>> LiteralPacket.parse(123, '101111111000101000111')
        ('000111', LiteralPacket (v: 123, val: 2021))
        """
        literal = ''
        while input[0] == '1':
            literal += input[1:5]
            input = input[5:]

        literal += input[1:5]
        input = input[5:]

        return input, cls(ver, binary_to_int(literal))


class GreaterThanPacket(ParentPacket):
    typ: ClassVar[int] = 5

    def __init__(self, ver):
        super().__init__(ver)

    def value(self) -> int:
        return 1 if self.sub_pkts[0].value() > self.sub_pkts[1].value() else 0


class LessThanPacket(ParentPacket):
    typ: ClassVar[int] = 6

    def __init__(self, ver):
        super().__init__(ver)

    def value(self) -> int:
        return 1 if self.sub_pkts[0].value() < self.sub_pkts[1].value() else 0


class EqualToPacket(ParentPacket):
    typ: ClassVar[int] = 7

    def __init__(self, ver):
        super().__init__(ver)

    def value(self) -> int:
        return 1 if self.sub_pkts[0].value() == self.sub_pkts[1].value() else 0


def parse_packets(packets_str: str) -> List[Packet]:
    packets = []
    while len(packets_str) > 6:
        packets_str, packet = parse_packet(packets_str)
        packets.append(packet)

    return packets


packet_types: List[Type[Packet]] = [
    SumPacket,
    ProductPacket,
    MinPacket,
    MaxPacket,
    LiteralPacket,
    GreaterThanPacket,
    LessThanPacket,
    EqualToPacket,
]

packet_type_mapping = {pkt.typ: pkt for pkt in packet_types}


def parse_packet(data: str) -> Tuple[str, Packet]:
    """
    >>> parse_packet('00111000000000000110111101000101001010010001001000000000')
    ('0000000', LessThanPacket (v: 1) [
      LiteralPacket (v: 6, val: 10)
      LiteralPacket (v: 2, val: 20)
    ])
    >>> parse_packet(ascii_to_binary('8A004A801A8002F478'))
    ('000', MinPacket (v: 4) [
      MinPacket (v: 1) [
        MinPacket (v: 5) [
          LiteralPacket (v: 6, val: 15)
        ]
      ]
    ])
    """
    data, ver = parse_int(data, 3)
    data, typ = parse_int(data, 3)
    if typ in packet_type_mapping:
        data, p = packet_type_mapping[typ].parse(ver, data)
    else:
        raise Exception(f'found packet with unknown type {typ}')

    return data, p


def main(arg: str):
    if exists(arg):
        with open(arg, 'r') as i:
            input = i.readline().strip()
            _, packet = parse_packet(ascii_to_binary(input))
    else:
        if arg.count('0') + arg.count('1') < len(arg):
            arg = ascii_to_binary(arg)
        _, packet = parse_packet(arg)
    print(packet)
    print(f'value: {packet.value()}')
    print(f'version sum: {packet.ver_sum()}')


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'
    main(input_file)
