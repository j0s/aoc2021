#!/bin/env python

from typing import List
import sys


def simulate(ages: List[int], days: int) -> List[int]:
    """
    >>> simulate([1], 0)
    [1]
    >>> simulate([1], 1)
    [0]
    >>> simulate([0], 1)
    [6, 8]
    """
    for d in range(days):
        new_fishes = ages.count(0)
        ages = list(map(lambda a: 6 if a == 0 else a-1, ages))
        ages.extend([8]*new_fishes)

    return ages


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    with open(input_file, 'r') as i:
        input = list(map(int, i.readline().strip().split(',')))
    result = simulate(input, 80)
    print(f'{len(result)}')
