#!/bin/env python

from typing import Dict
import sys


def simulate(ages: Dict[int, int], days: int) -> Dict[int, int]:
    """
    >>> simulate({1: 1}, 0)
    {1: 1}
    >>> simulate({1: 1}, 1)
    {0: 1}
    >>> simulate({1: 1}, 2)
    {6: 1, 8: 1}
    >>> simulate({0: 1}, 1)
    {6: 1, 8: 1}
    """
    for d in range(days):
        print(d)
        print(ages)
        new_ages: Dict[int, int] = {}
        for k, v in ages.items():
            if v == 0:
                continue
            elif k == 0:
                new_ages[6] = new_ages.get(6, 0) + v
                new_ages[8] = v
            else:
                new_ages[k-1] = new_ages.get(k-1, 0) + v
        ages = new_ages

    return ages


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    with open(input_file, 'r') as i:
        input = list(map(int, i.readline().strip().split(',')))
    initial_fishes: Dict[int, int] = {}
    for num in input:
        initial_fishes[num] = initial_fishes.get(num, 0) + 1
    result = simulate(initial_fishes, 256)
    print(f'{result}, sum: {sum(v for v in result.values())}')
