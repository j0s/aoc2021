#!/bin/env python

from typing import Tuple, List
import sys
from os.path import exists


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


def parse_literal(input: str) -> Tuple[str, int]:
    """
    >>> parse_literal('101111111000101000111')
    ('000111', 2021)
    """
    literal = ''
    while input[0] == '1':
        literal += input[1:5]
        input = input[5:]

    literal += input[1:5]
    input = input[5:]

    return input, binary_to_int(literal)


def parse_int(input: str, len: int) -> Tuple[str, int]:
    return input[len:], binary_to_int(input[:len])


class Packet(object):
    Literal = 4

    def __init__(self, ver: int, typ: int):
        self.ver = ver
        self.typ = typ
        self.literal: int | None = None
        self.operator: int | None = None
        self.sub_pkts: List[Packet] = []

    def __repr__(self) -> str:
        if self.typ == Packet.Literal:
            return f'lit (v: {self.ver}, lit: {self.literal})'
        else:
            sub_pkts_str = '['
            for pkt in self.sub_pkts:
                for line in pkt.__repr__().split('\n'):
                    sub_pkts_str += '\n  ' + line
            sub_pkts_str += '\n]'
            return f'op  (v: {self.ver}, oper: {self.operator}) {sub_pkts_str}'

    def ver_sum(self) -> int:
        return self.ver + sum([p.ver_sum() for p in self.sub_pkts])


def parse_packets(packets_str: str) -> List[Packet]:
    packets = []
    while len(packets_str) > 6:
        packets_str, packet = parse_packet(packets_str)
        packets.append(packet)

    return packets


def parse_packet(packet: str) -> Tuple[str, Packet]:
    """
    parse_packet('00111000000000000110111101000101001010010001001000000000')
    parse_packet(ascii_to_binary('8A004A801A8002F478'))
    """
    line, ver = parse_int(packet, 3)
    line, typ = parse_int(line, 3)
    p = Packet(ver, typ)
    if typ == Packet.Literal:
        line, literal = parse_literal(line)
        p.literal = literal
    else:
        p.operator = typ
        line, len_type_id = parse_int(line, 1)
        if len_type_id == 0:
            line, sub_pkt_len = parse_int(line, 15)
            p.sub_pkts = parse_packets(line[:sub_pkt_len])
            line = line[sub_pkt_len:]
        elif len_type_id == 1:
            line, num_sub_pkts = parse_int(line, 11)
            for n in range(num_sub_pkts):
                line, pkt = parse_packet(line)
                p.sub_pkts.append(pkt)

    return line, p


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
    print(f'version sum: {packet.ver_sum()}')


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'
    main(input_file)
