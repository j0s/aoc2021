#!/bin/env python

from typing import List, Tuple
import sys


def valid_y_speeds(min_y: int, max_y: int) -> List[int]:
    valid_speeds = []
    for initial_speed in range(min_y - 1, 1000):
        speed = initial_speed
        y = 0
        while y >= min_y:
            if y <= max_y:
                valid_speeds.append(initial_speed)
                break
            y += speed
            speed -= 1

    return valid_speeds


def valid_x_speeds(min_x: int, max_x: int) -> List[int]:
    valid_speeds = []
    for initial_speed in range(1, 1000):
        speed = initial_speed
        x = 0
        while x <= max_x:
            if x >= min_x:
                valid_speeds.append(initial_speed)
                break
            x += speed
            speed -= 1
            if speed == 0:
                break
    print(valid_speeds)
    return valid_speeds


def valid_speed(min_x, max_x, min_y, max_y, x_speed: int,
                y_speed: int) -> bool:
    x, y = 0, 0
    while x <= max_x and y >= min_y:
        # print(x, x_speed, min_x, max_x)
        # print(y, y_speed, min_y, max_y)
        if y <= max_y and x >= min_x:
            return True
        y += y_speed
        y_speed -= 1
        x += x_speed
        x_speed -= 1 if x_speed > 0 else 0
    return False


def valid_speeds(min_x, max_x, min_y, max_y, x_speeds: List[int],
                 y_speeds: List[int]) -> List[Tuple[int, int]]:
    speeds = []
    for x_speed in x_speeds:
        for y_speed in y_speeds:
            if valid_speed(min_x, max_x, min_y, max_y, x_speed, y_speed):
                speeds.append((x_speed, y_speed))

    return speeds


def main(arg: str):
    with open(arg, 'r') as i:
        input = i.readline().strip()
        x_str, y_str = input[13:].split(', ')
        min_x, max_x = [int(x) for x in x_str[2:].split('..')]
        min_y, max_y = [int(y) for y in y_str[2:].split('..')]
        y_speeds = valid_y_speeds(min_y, max_y)
        x_speeds = valid_x_speeds(min_x, max_x)
        s = valid_speeds(min_x, max_x, min_y, max_y, x_speeds, y_speeds)
        print(s)
        print(len(s))


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'
    main(input_file)
