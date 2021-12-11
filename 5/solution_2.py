from typing import Dict, NamedTuple, List
import sys


class Coord(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f'({self.x}, {self.y})'


def get_line_coords(start: Coord, end: Coord) -> List[Coord]:
    """
    >>> get_line_coords(Coord(0,0), Coord(2,2))
    [(0, 0), (1, 1), (2, 2)]
    >>> get_line_coords(Coord(2,2), Coord(0,0))
    [(0, 0), (1, 1), (2, 2)]
    >>> get_line_coords(Coord(0,2), Coord(2,0))
    [(0, 2), (1, 1), (2, 0)]
    >>> get_line_coords(Coord(2,0), Coord(0,2))
    [(0, 2), (1, 1), (2, 0)]
    >>> get_line_coords(Coord(0,2), Coord(2,2))
    [(0, 2), (1, 2), (2, 2)]
    >>> get_line_coords(Coord(2,2), Coord(0,2))
    [(0, 2), (1, 2), (2, 2)]
    >>> get_line_coords(Coord(2,0), Coord(2,2))
    [(2, 0), (2, 1), (2, 2)]
    >>> get_line_coords(Coord(2,2), Coord(2,0))
    [(2, 0), (2, 1), (2, 2)]
    """
    x_values = list(range(min(start.x, end.x), max(start.x, end.x)+1))
    y_values = list(range(min(start.y, end.y), max(start.y, end.y)+1))
    if start.x > end.x:
        x_values.reverse()
    if start.y > end.y:
        y_values.reverse()

    if len(x_values) == 1:
        x_values = [x_values[0]]*len(y_values)

    if len(y_values) == 1:
        y_values = [y_values[0]]*len(x_values)

    coords = [Coord(x, y) for x, y in zip(x_values, y_values)]
    coords.sort()
    return coords


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
            for c in get_line_coords(Coord(start_x, start_y), Coord(end_x, end_y)):
                coords[c] = coords.setdefault(c, 0) + 1
    print(f'{len(list(filter(lambda v: v >=2, coords.values())))}')
