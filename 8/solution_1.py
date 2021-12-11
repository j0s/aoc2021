#!/bin/env python

from typing import Dict, List, Set
import sys

all_positions = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}


def decode(patterns: List[str], output: List[str]) -> List[int]:
    candidates: Dict[str, Set[str]] = {
        pos: all_positions for pos in all_positions}

    for p in patterns:
        if len(p) == 2:
            for i in range(2):
                candidates[p[i]] &= {'c', 'f'}
        elif len(p) == 3:
            for i in range(3):
                candidates[p[i]] &= {'a', 'c', 'f'}
        elif len(p) == 4:
            for i in range(4):
                candidates[p[i]] &= {'b', 'c', 'd', 'f'}

    print(candidates)

    return [1]


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    positions: List[int] = []
    all_outputs: List[str] = []
    with open(input_file, 'r') as i:
        for line in i:
            all_outputs.extend(line.strip().split('|')[1].strip().split())

    print(f'{len([o for o in all_outputs if len(o) in [2, 3, 4, 7]])}')
