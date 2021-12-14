#!/bin/env python

from typing import Set, Tuple
import sys


def fold(dots: Set[Tuple[int, int]], axis: str, pos: int):
    if axis == 'y':
        for x, y in dots.copy():
            if y > pos:
                dots.add((x, pos - (y - pos)))
                dots.remove((x, y))
    elif axis == 'x':
        for x, y in dots.copy():
            if x > pos:
                dots.add((pos - (x - pos), y))
                dots.remove((x, y))


def plot(dots: Set[Tuple[int, int]]):
    max_x = max([x for (x, y) in dots])
    max_y = max([y for (x, y) in dots])
    rows = []
    for y in range(max_y + 1):
        rows.append(''.join('#' if (x, y) in dots else '-'
                            for x in range(max_x + 1)))
    print('\n'.join(rows))


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    dots: Set[Tuple[int, int]] = set()
    with open(input_file, 'r') as i:
        while (line := i.readline().strip()) != '':
            x, y = map(int, line.split(','))
            dots.add((x, y))
        print(f'created {len(dots)} dots')
        while (line := i.readline().strip()) != '':
            axis, pos_str = line.split()[2].split('=')
            pos = int(pos_str)
            fold(dots, axis, pos)
            print(f'remaining after folding at {axis}={pos}: {len(dots)} dots')
    plot(dots)
