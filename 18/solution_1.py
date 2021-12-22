#!/bin/env python

from __future__ import annotations
from typing import Tuple
import sys


class Pair:
    def __init__(self,
                 x: Pair | int = 0,
                 y: Pair | int = 0,
                 parent: Pair = None):
        """
        >>> print(Pair(1, Pair(Pair(2, 3), Pair(4, 5))))
        [1,[[2,3],[4,5]]]
        """
        self.parent: Pair | None = parent
        self.x: int | Pair = x
        if isinstance(x, Pair):
            x.parent = self
        self.y: int | Pair = y
        if isinstance(y, Pair):
            y.parent = self

    def __repr__(self) -> str:
        return f'[{self.x},{self.y}]'

    def add(self, other: Pair) -> Pair:
        return Pair(self, other)

    def explode(self):
        """
        >>> p = Pair.parse('[[[[[9,8],1],2],3],4]')[0]
        >>> p.reduce() and p
        [[[[0,9],2],3],4]
        >>> p = Pair.parse('[7,[6,[5,[4,[3,2]]]]]')[0]
        >>> p.reduce() and p
        [7,[6,[5,[7,0]]]]
        >>> p = Pair.parse('[[6,[5,[4,[3,2]]]],1]')[0]
        >>> p.reduce() and p
        [[6,[5,[7,0]]],3]
        """
        if isinstance(self.x, Pair) or isinstance(self.y, Pair):
            raise Exception('tried to explode pair that '
                            f'contained another pair: {self}')
        if self.parent is None:
            raise Exception('tried to explode pair that '
                            f'does not have a parent: {self}')
        # the pair's left value is added to the first regular
        # number to the left of the exploding pair (if any)
        left_pair = self.left()
        if left_pair:
            left_pair.x += self.x
        right_pair = self.right()
        if right_pair:
            right_pair.y += self.y
        if self == self.parent.y:  # self is right
            self.parent.y = 0
        elif self == self.parent.x:
            # self.parent.y += self.y
            self.parent.x = 0

    def left(self) -> Pair | None:
        assert self.parent
        p = self
        while p.parent and p.parent.x == p:
            p = p.parent
        return p

    def right(self) -> Pair | None:
        assert self.parent
        p = self
        while p.parent and p.parent.y == p:
            p = p.parent
        return p

    def reduce(self, depth: int = 0) -> bool:
        if depth == 4:
            self.explode()
            return True
        elif isinstance(self.x, int) and self.x >= 10:
            self.x = Pair.split(self.x)
            return True
        elif isinstance(self.y, int) and self.y >= 10:
            self.y = Pair.split(self.y)
            return True
        elif isinstance(self.x, Pair) and self.x.reduce(depth + 1):
            return True
        elif isinstance(self.y, Pair) and self.y.reduce(depth + 1):
            return True
        return False

    @staticmethod
    def parse(s: str) -> Tuple[Pair, int]:
        """
        >>> Pair.parse('[[[[[9,8],1],2],3],4]')[0]
        [[[[[9,8],1],2],3],4]
        >>> Pair.parse('[7,[6,[5,[4,[3,2]]]]]')[0]
        [7,[6,[5,[4,[3,2]]]]]
        """
        p = Pair()
        comma_read = False
        i = 1  # skip initial '['
        while i < len(s):
            char = s[i]
            if char == '[':
                if comma_read:
                    p.y, chars_read = Pair.parse(s[i:])
                    p.y.parent = p
                    i += chars_read
                else:
                    p.x, chars_read = Pair.parse(s[i:])
                    p.x.parent = p
                    i += chars_read
            elif char == ']':
                return p, i + 1
            elif char == ',':
                comma_read = True
                i += 1
            elif char.isnumeric():
                if comma_read:
                    p.y = int(char)
                    i += 1
                else:
                    p.x = int(char)
                    i += 1

    @staticmethod
    def split(v: int) -> Pair:
        """
        >>> Pair.split(10)
        [5,5]
        >>> Pair.split(11)
        [5,6]
        """
        return Pair(int(v / 2), int((v + 1) / 2))


def main(arg: str):
    with open(arg, 'r') as i:
        input = i.readline().strip()


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'
    main(input_file)
