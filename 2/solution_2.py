from typing import List


def get_increasing_depths(depths: List[int]) -> int:
    increasing: int = 0
    for i, depth in enumerate(depths[:-1], 1):
        if depths[i] > depth:
            increasing += 1
    return increasing


if __name__ == '__main__':
    aim: int = 0
    depth: int = 0
    horizontal_pos: int = 0
    with open('input', 'r') as i:
        for line in i:
            verb, amount = line.split()
            if verb == 'up':
                aim -= int(amount)
            elif verb == 'down':
                aim += int(amount)
            elif verb == 'forward':
                horizontal_pos += int(amount)
                depth += (aim * int(amount))

    print(f'{depth * horizontal_pos}')
