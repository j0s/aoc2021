#!/bin/env python

from typing import Dict
import sys


def update_polymer(polymer: str, updates: Dict[str, str]) -> str:
    result: str = ''
    for i in range(len(polymer) - 1):
        pair = polymer[i] + polymer[i + 1]
        if pair in updates:
            result += polymer[i] + updates[pair]
        else:
            result += polymer[i]
    result += polymer[-1]

    return result


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    updates: Dict[str, str] = {}
    with open(input_file, 'r') as f:
        polymer = f.readline().strip()
        for line in f:
            line = line.strip()
            if line == '':
                continue
            substr, insert = line.split(' -> ')
            updates[substr] = insert

    print(f'template: {polymer}')
    for i in range(10):
        polymer = update_polymer(polymer, updates)
        print(f'after step {i + 1}: {polymer}')

    frequencies: Dict[str, int] = {}
    for char in polymer:
        if char not in frequencies:
            frequencies[char] = 0
        frequencies[char] += 1
    most_frequent = max(frequencies.values())
    least_frequent = min(frequencies.values())
    print(f'answer: {most_frequent - least_frequent}')
