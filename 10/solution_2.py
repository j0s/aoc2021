#!/bin/env python

from typing import List, Dict, Tuple
import sys


char_pairs: Dict[str, str] = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>',
}


def corrupt_line(line: str) -> bool:
    """
    >>> corrupt_line('{([(<{}[<>[]}>{[]{[(<()>')
    True
    >>> corrupt_line('[<>({}){}[([])<>]]')
    False
    """
    stack: List[str] = []
    for char in line:
        if char in '([{<':
            stack.append(char)
        elif char in ')]}>':
            last_opened_char = stack.pop()
            if char_pairs[last_opened_char] != char:
                return True

    return False


def missing_tokens(line: str) -> str:
    """
    >>> missing_tokens('[<>({}){}[([])<>]]')
    ''
    >>> missing_tokens('[({(<(())[]>[[{[]{<()<>>')
    '}}]])})]'
    >>> missing_tokens('[(()[<>])]({[<{<<[]>>(')
    ')}>]})'
    >>> missing_tokens('(((({<>}<{<{<>}{[]{[]{}')
    '}}>}>))))'
    >>> missing_tokens('{<[[]]>}<{[{[{[]{()[[[]')
    ']]}}]}]}>'
    >>> missing_tokens('<{([{{}}[<[[[<>{}]]]>[]]')
    '])}>'

    """
    stack: List[str] = []
    for char in line:
        if char in '([{<':
            stack.append(char)
        elif char in ')]}>':
            last_opened_char = stack.pop()
            if char_pairs[last_opened_char] != char:
                print('found corrupt line!')
                exit(-1)

    return ''.join([char_pairs[c] for c in reversed(stack)])


def score(tokens: str) -> int:
    char_points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    score = 0
    for t in tokens:
        score *= 5
        score += char_points[t]

    return score


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    scores: List[int] = []
    with open(input_file, 'r') as i:
        for line in i:
            if corrupt_line(line):
                continue
            tokens = missing_tokens(line)
            scores.append(score(tokens))

    scores = sorted(scores)
    print(f'{scores[int((len(scores) - 1) / 2)]}')
