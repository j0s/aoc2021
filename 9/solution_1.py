#!/bin/env python

from typing import List
import sys


def low_points(height_map: List[List[int]]) -> List[int]:
    x_max = len(height_map[0])
    y_max = len(height_map)

    low_points: List[int] = []
    for y in range(y_max):
        for x in range(x_max):
            print(x, y)
            if ((y == 0 or height_map[y-1][x] > height_map[y][x]) and
                (y == y_max-1 or height_map[y+1][x] > height_map[y][x]) and
                (x == 0 or height_map[y][x-1] > height_map[y][x]) and
                    (x == x_max-1 or height_map[y][x+1] > height_map[y][x])):
                low_points.append(height_map[y][x])

    return low_points


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    height_map: List[List[int]] = []
    with open(input_file, 'r') as i:
        for line in i:
            height_map.append([int(c) for c in line.strip()])

    points = low_points(height_map)

    print(f'points: {points}')
    print(f'{sum([p+1 for p in points])}')
