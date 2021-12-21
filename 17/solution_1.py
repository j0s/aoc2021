#!/bin/env python

import sys


def main(arg: str):
    with open(arg, 'r') as i:
        input = i.readline().strip()
        _, y_str = input[13:].split(', ')
        min_y, _ = [int(y) for y in y_str[2:].split('..')]
        # Velocity i y and x are independent, so just focus on y for now.
        # The path is symmetric, so on the way down the projectile will
        # be at y=0 at some point, with the same speed as the inital speed,
        # but negative. To maximize height we want to maximize initial
        # speed, so the speed should be such that the projectile moves from
        # y=0 to y=min_y in one step. This means the speed should be min_y-0-1.
        # Calculating y for vel_y=0 we can take advantage of the fact that
        # it is a triangular number https://en.wikipedia.org/wiki/Triangular_number
        vel_y = 0 - min_y - 1
        max_y = vel_y * (vel_y + 1) / 2
        print(max_y)


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'
    main(input_file)
