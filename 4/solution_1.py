from typing import List, Set
import sys


class Game(object):
    def __init__(self, board_no: int, numbers: List[List[int]]):
        self.board_no = board_no
        self.rows: List[Set[int]] = []
        self.columns: List[Set[int]] = []
        for row in numbers:
            self.rows.append(set(row))
        for i in range(len(numbers[0])):
            self.columns.append(set([row[i] for row in numbers]))

    def draw(self, number: int) -> bool:
        for row, col in zip(self.rows, self.columns):
            row.discard(number)
            col.discard(number)

        for row, col in zip(self.rows, self.columns):
            if len(row) == 0 or len(col) == 0:
                print(f'game {self.board_no} won after drawing {number}!')
                print(
                    f'remaining numbers: {self.remaining_numbers()}')
                return True
        return False

    def remaining_numbers(self) -> List[int]:
        numbers: Set[int] = set()
        for row in self.rows + self.columns:
            numbers |= row
        return list(numbers)

    def remaining_points(self) -> int:
        return sum(self.remaining_numbers())


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    games: List[Game] = []
    with open(input_file, 'r') as i:
        draws = [int(token) for token in i.readline().strip().split(',')]
        current_game: List[List[int]] = []
        for line in i:
            line = line.strip()
            if len(line) == 0:
                if len(current_game) > 0:
                    games.append(Game(len(games)+1, current_game))
                current_game = []
                continue
            current_game.append([int(token) for token in line.split()])
        if len(current_game) > 0:
            games.append(Game(len(games)+1, current_game))

    for draw in draws:
        for game in games:
            if game.draw(draw):
                print(
                    f'final score: {game.remaining_points()} * {draw} = {game.remaining_points() * draw}')
                exit(0)
