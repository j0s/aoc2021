from typing import List


def get_increasing_depths(depths: List[int]) -> int:
    increasing: int = 0
    for i, depth in enumerate(depths[:-3], 3):
        if depths[i] > depth:
            increasing += 1
    return increasing


if __name__ == '__main__':
    depths: List[int] = []
    with open('input', 'r') as i:
        for line in i:
            depths.append(int(line))
    print(f'increasing: {get_increasing_depths(depths)}')
