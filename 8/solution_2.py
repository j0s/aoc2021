#!/bin/env python

from typing import Dict, List
import sys

all_numbers: Dict[str, int] = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}


def decode(patterns: List[str], output: List[str]) -> int:
    one = set(list(filter(lambda p: len(p) == 2, patterns))[0])
    seven = set(list(filter(lambda p: len(p) == 3, patterns))[0])
    four = set(list(filter(lambda p: len(p) == 4, patterns))[0])
    eight = set(list(filter(lambda p: len(p) == 7, patterns))[0])
    frequencies: Dict[str, int] = {}
    for p in patterns:
        for char in p:
            frequencies[char] = frequencies.get(char, 0) + 1

    a = (seven - one).pop()
    b = [k for (k, v) in frequencies.items() if v == 6][0]
    c = [k for (k, v) in frequencies.items() if v == 8 and k != a][0]
    e = [k for (k, v) in frequencies.items() if v == 4][0]
    f = [k for (k, v) in frequencies.items() if v == 9][0]
    g = (eight - four - {a, e}).pop()
    d = [k for (k, v) in frequencies.items() if v == 7 and k != g][0]

    decoder = {
        a: 'a',
        b: 'b',
        c: 'c',
        d: 'd',
        e: 'e',
        f: 'f',
        g: 'g',
    }

    decoded_output: List[str] = []
    for o in output:
        decoded_output.append(''.join(sorted([decoder[char] for char in o])))

    return all_numbers[decoded_output[0]] * 1000 + \
        all_numbers[decoded_output[1]] * 100 + \
        all_numbers[decoded_output[2]] * 10 + \
        all_numbers[decoded_output[3]] * 1


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    positions: List[int] = []
    total = 0
    with open(input_file, 'r') as i:
        for line in i:
            patterns_str, output_str = line.strip().split('|')
            scrambled_patterns = patterns_str.strip().split()
            scrambled_output = output_str.strip().split()
            real_output = decode(scrambled_patterns, scrambled_output)
            total += real_output
            print(real_output)
    print(f'sum: {total}')
