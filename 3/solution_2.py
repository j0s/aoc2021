from typing import List, Callable
import sys

Binary = List[int]


def decimal(binary: Binary) -> int:
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


def filter_candidates(candidates: List[Binary],
                      get_filter_pos: Callable[[int, List[Binary]], int]) -> Binary:
    """
    >>> find_by_mask([1, 1, 0], [[1, 1, 0, 1], [1, 1, 1, 0], [0, 1, 0, 1]])
    [1, 1, 0, 1]
    """
    i = 0
    while len(candidates) > 1:
        candidates = list(filter(lambda e: e[i] == get_filter_pos(
            i, candidates), candidates))
        i += 1
    return candidates[0]


def most_common(i: int, report: List[Binary]) -> int:
    return 1 if sum([row[i] if row[i] == 1 else -1 for row in report]) >= 0 else 0


def least_common(i: int, report: List[Binary]) -> int:
    m = most_common(i, report)
    return 0 if m else 1


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    diagnostic_report: List[Binary] = []
    with open(input_file, 'r') as i:
        for line in i:
            row = [int(token) for token in line.strip()]
            diagnostic_report.append(row)
    o2_generator_rating = filter_candidates(diagnostic_report, most_common)
    print(f'o2_generator_rating: {o2_generator_rating}')
    co2_scrubber_rating = filter_candidates(diagnostic_report, least_common)
    print(f'co2_scrubber_rating: {co2_scrubber_rating}')
    result = decimal(o2_generator_rating) * \
        decimal(co2_scrubber_rating)
    print(f'{result}')
