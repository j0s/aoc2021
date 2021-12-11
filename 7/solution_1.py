#!/bin/env python

from typing import List, Dict
import sys


def total_distance(sub_positions: List[int], target_position: int) -> int:
    """
    >>> total_distance([0,2], 1)
    2
    """
    return sum(abs(pos - target_position) for pos in sub_positions)


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    positions: List[int] = []
    with open(input_file, 'r') as i:
        positions = list(map(int, i.readline().strip().split(',')))
    candidates: Dict[int, int] = {target: total_distance(
        positions, target) for target in range(min(positions), max(positions)+1)}
    distances = candidates.values()

    print(f'{min(distances)}')
