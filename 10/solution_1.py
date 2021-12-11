#!/bin/env python

from typing import List, Dict, Tuple
import sys


def parse_line(line: str) -> Tuple[str, bool]:
    """
    >>> parse_line('{([(<{}[<>[]}>{[]{[(<()>')
    ('}', True)
    """
    char_pairs: Dict[str, str] = {
        '(': ')',
        '{': '}',
        '[': ']',
        '<': '>',
    }
    stack: List[str] = []
    for char in line:
        if char in '([{<':
            stack.append(char)
        elif char in ')]}>':
            last_opened_char = stack.pop()
            if char_pairs[last_opened_char] != char:
                return char, True

    return "", False


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    char_points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    illegal_chars: List[str] = []
    with open(input_file, 'r') as i:
        for line in i:
            first_illegal_char, found = parse_line(line)
            if found:
                illegal_chars.append(first_illegal_char)

    print(f'{sum([char_points[c] for c in illegal_chars])}')
