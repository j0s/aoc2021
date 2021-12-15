#!/bin/env python

from typing import Dict, Tuple
import sys


def update_polymer(pair_frequencies: Dict[str, int],
                   char_frequencies: Dict[str, int],
                   updates: Dict[str, str]) -> Dict[str, int]:
    print(f'before: {pair_frequencies}')
    updated: Dict[str, int] = {}
    for pair, number in pair_frequencies.items():
        # print(f'{pair[0] + updates[pair]}={number}')
        # print(f'{updates[pair] + pair[1]}={number}')
        pair_1 = pair[0] + updates[pair]
        if pair_1 not in updated:
            updated[pair_1] = 0
        updated[pair_1] += number

        pair_2 = updates[pair] + pair[1]
        if pair_2 not in updated:
            updated[pair_2] = 0
        updated[pair_2] += number

        if not updates[pair] in char_frequencies:
            char_frequencies[updates[pair]] = 0
        char_frequencies[updates[pair]] += number
    print(f'after: {updated}')
    return updated


def parse_polymer(polymer: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    pair_frequencies: Dict[str, int] = {}
    char_frequencies: Dict[str, int] = {}
    for i in range(len(polymer) - 1):
        pair = polymer[i] + polymer[i + 1]
        if pair not in pair_frequencies:
            pair_frequencies[pair] = 0
        pair_frequencies[pair] += 1
    for char in polymer:
        if char not in char_frequencies:
            char_frequencies[char] = 0
        char_frequencies[char] += 1

    return pair_frequencies, char_frequencies


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    pair_frequencies: Dict[str, int] = {}
    char_frequencies: Dict[str, int] = {}
    updates: Dict[str, str] = {}
    with open(input_file, 'r') as f:
        polymer = f.readline().strip()
        pair_frequencies, char_frequencies = parse_polymer(polymer)
        for line in f:
            line = line.strip()
            if line == '':
                continue
            substr, insert = line.split(' -> ')
            updates[substr] = insert

    for i in range(40):
        pair_frequencies = update_polymer(pair_frequencies, char_frequencies,
                                          updates)

    most_frequent = max(char_frequencies.values())
    least_frequent = min(char_frequencies.values())

    print(f'frequencies: {char_frequencies}')
    print(f'answer: {most_frequent - least_frequent}')
