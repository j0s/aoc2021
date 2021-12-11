from typing import List


if __name__ == '__main__':
    depth_moves: List[int] = []
    fwd_moves: List[int] = []
    with open('input', 'r') as i:
        for line in i:
            verb, amount = line.split()
            if verb == 'up':
                depth_moves.append(-int(amount))
            elif verb == 'down':
                depth_moves.append(int(amount))
            elif verb == 'forward':
                fwd_moves.append(int(amount))
    total_depth = sum(depth_moves)
    horiz_pos = sum(fwd_moves)
    print(f'{total_depth} * {horiz_pos}: {total_depth * horiz_pos}')
