#!/bin/env python

from typing import List
import sys


def increase_energy_level(levels: List[List[int]]) -> int:
    flashes = 0
    for row_ix, row in enumerate(levels):
        for col_ix, _ in enumerate(row):
            levels[row_ix][col_ix] += 1
            flashes += maybe_flash(levels, row_ix, col_ix)
    return flashes


def reset_flashed(levels: List[List[int]]):
    for row_ix, row in enumerate(levels):
        for col_ix, _ in enumerate(row):
            if levels[row_ix][col_ix] > 9:
                levels[row_ix][col_ix] = 0


def increase(levels: List[List[int]], row_ix: int, col_ix: int) -> int:
    levels[row_ix][col_ix] += 1
    return maybe_flash(levels, row_ix, col_ix)


def maybe_flash(levels: List[List[int]], row_ix: int, col_ix: int) -> int:
    if levels[row_ix][col_ix] != 10:
        return 0

    flashes = 1
    levels[row_ix][col_ix] += 1
    if row_ix > 0:
        flashes += increase(levels, row_ix - 1, col_ix)
        if col_ix > 0:
            flashes += increase(levels, row_ix - 1, col_ix - 1)
        if col_ix < len(levels[row_ix]) - 1:
            flashes += increase(levels, row_ix - 1, col_ix + 1)
    if row_ix < len(levels) - 1:
        flashes += increase(levels, row_ix + 1, col_ix)
        if col_ix > 0:
            flashes += increase(levels, row_ix + 1, col_ix - 1)
        if col_ix < len(levels[row_ix]) - 1:
            flashes += increase(levels, row_ix + 1, col_ix + 1)
    if col_ix > 0:
        flashes += increase(levels, row_ix, col_ix - 1)
    if col_ix < len(levels[0]) - 1:
        flashes += increase(levels, row_ix, col_ix + 1)
    return flashes


def calculate_day(levels: List[List[int]]) -> int:
    flashes = increase_energy_level(levels)
    reset_flashed(levels)

    return flashes


def bold(val: int) -> str:
    return f'\033[1m{val}\033[0m'


def print_levels(levels: List[List[int]]) -> str:
    return '\n'.join([
        ''.join([str(val) if val != 0 else bold(val) for val in row])
        for row in levels
    ])


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    levels: List[List[int]] = []
    with open(input_file, 'r') as i:
        for line in i:
            line = line.strip()
            if line == '':
                continue
            levels.append([int(char) for char in line])

    total_flashes = 0
    print(f'original values:\n{print_levels(levels)}\n')
    for day in range(100):
        total_flashes += calculate_day(levels)
        print(f'after day {day+1}:\n{print_levels(levels)}\n')
    print(f'total flashes: {total_flashes}')
