#!/bin/env python

from typing import List, Dict
import sys


def fuel_used(distance: int) -> int:
    """
    >>> fuel_used(1)
    1
    >>> fuel_used(2)
    3
    >>> fuel_used(3)
    6
    >>> fuel_used(4)
    10
    """
    return int(distance*(distance+1)/2)


def total_distance(sub_positions: List[int], target_position: int) -> int:
    """
    >>> total_distance([0,2], 1)
    2
    """
    return sum(fuel_used(abs(pos - target_position)) for pos in sub_positions)


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
