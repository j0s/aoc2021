from typing import List
import sys


def binary_xor(binary: List[int]) -> List[int]:
    """
    >>> binary_xor([0, 1, 0, 1])
    [1, 0, 1, 0]
    """
    return [0 if v else 1 for v in binary]


def get_decimal_value(binary: List[int]) -> int:
    """
    >>> get_decimal_value([0, 0, 0, 0])
    0
    >>> get_decimal_value([1, 0, 0, 0])
    8
    >>> get_decimal_value([1, 1, 1, 1])
    15
    """
    dec = 0
    for i, v in enumerate(reversed(binary)):
        dec += v*(2**i)
    return dec


def get_gamma_rate(report: List[List[int]]) -> List[int]:
    """
    >>> get_gamma_rate([[0, 1, 0, 1], [0, 0, 1, 1]])
    [0, 1, 1, 1]
    """
    gamma_rate = [0]*len(report[0])
    for row in report:
        for i, value in enumerate(row):
            gamma_rate[i] += 1 if value == 1 else -1

    return [0 if r < 0 else 1 for r in gamma_rate]


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    diagnostic_report: List[List[int]] = []
    fwd_moves: List[int] = []
    with open('input', 'r') as i:
        for line in i:
            row = [int(token) for token in line.strip()]
            diagnostic_report.append(row)
    gamma = get_gamma_rate(diagnostic_report)
    epsilon = binary_xor(gamma)
    result = get_decimal_value(gamma) * get_decimal_value(epsilon)
    print(f'{result}')
