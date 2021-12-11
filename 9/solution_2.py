#!/bin/env python

from typing import List, Tuple, Set
from functools import reduce
import sys


def basin(height_map: List[List[int]],
          low_point: Tuple[int, int],
          visited_points: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    y, x = low_point
    if (y == len(height_map) or y == -1 or
        x == len(height_map[0]) or x == -1 or
        height_map[y][x] == 9 or
            (y, x) in visited_points):
        return set()
    else:
        visited_points |= {(y, x)}
        return ({(y, x)} |
                basin(height_map, (y-1, x), visited_points) |
                basin(height_map, (y+1, x), visited_points) |
                basin(height_map, (y, x-1), visited_points) |
                basin(height_map, (y, x+1), visited_points))


def basin_size(height_map: List[List[int]], low_point: Tuple[int, int]) -> int:
    return len(basin(height_map, low_point, set()))


def low_points(height_map: List[List[int]]) -> List[Tuple[int, int]]:
    x_max = len(height_map[0])
    y_max = len(height_map)

    low_points: List[Tuple[int, int]] = []
    for y in range(y_max):
        for x in range(x_max):
            print(x, y)
            if ((y == 0 or height_map[y-1][x] > height_map[y][x]) and
                (y == y_max-1 or height_map[y+1][x] > height_map[y][x]) and
                (x == 0 or height_map[y][x-1] > height_map[y][x]) and
                    (x == x_max-1 or height_map[y][x+1] > height_map[y][x])):
                low_points.append((y, x))

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

    print(reduce(lambda x, y: x*y,
          sorted([basin_size(height_map, b) for b in points])[-3:]))
