from typing import Dict, NamedTuple
import sys


class Coord(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f'({self.x}, {self.y})'


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    coords: Dict[Coord, int] = {}
    with open(input_file, 'r') as i:
        for line in i:
            line = line.strip()
            start, _, end = line.split()
            start_x, start_y = map(int, start.split(','))
            end_x, end_y = map(int, end.split(','))
            if start_x > end_x:
                start_x, end_x = end_x, start_x
            if start_y > end_y:
                start_y, end_y = end_y, start_y
            if start_x != end_x and start_y != end_y:
                print(f'skipping line {line}, neither vertical nor horizontal')
                continue
            print(f'adding line {start_y},{start_x}->{end_y},{end_x}')
            for y in range(start_y, end_y+1):
                for x in range(start_x, end_x+1):
                    c = Coord(x, y)
                    coords[c] = coords.setdefault(c, 0) + 1
    print(f'{len([v for v in coords.values() if v >= 2])}')
