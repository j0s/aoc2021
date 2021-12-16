#!/bin/env python

from typing import List
import sys


class Node(object):
    def __init__(self, x: int, y: int, weight: int):
        self.x: int = x
        self.y: int = y
        self.weight: int = weight
        self.distance: int = sys.maxsize
        self.prev: Node | None = None

    def __repr__(self) -> str:
        return (
            f'(x: {self.x}, y: {self.y}, w: {self.weight}, '
            f'd: {self.distance if self.distance != sys.maxsize else None})')


def next_node(unvisited: List[Node]) -> Node:
    next = min(unvisited, key=lambda x: x.distance)
    unvisited.remove(next)
    return next


def neighbors(y_x_nodes: List[List[Node]], node: Node) -> List[Node]:
    nbrs: List[Node] = []
    if node.y > 0:
        nbrs.append(y_x_nodes[node.y - 1][node.x])
        # if diagonally:
        # if node.x > 0:
        #     nbrs.append(y_x_nodes[node.y - 1][node.x - 1])
        # if node.x < len(y_x_nodes[0]) - 1:
        #     nbrs.append(y_x_nodes[node.y - 1][node.x + 1])
    if node.y < len(y_x_nodes) - 1:
        nbrs.append(y_x_nodes[node.y + 1][node.x])
        # if diagonally:
        # if node.x > 0:
        #     nbrs.append(y_x_nodes[node.y + 1][node.x - 1])
        # if node.x < len(y_x_nodes[0]) - 1:
        #     nbrs.append(y_x_nodes[node.y + 1][node.x + 1])
    if node.x > 0:
        nbrs.append(y_x_nodes[node.y][node.x - 1])
    if node.x < len(y_x_nodes[0]) - 1:
        nbrs.append(y_x_nodes[node.y][node.x + 1])
    return nbrs


def shortest_path(y_x_nodes: List[List[Node]], nodes: List[Node],
                  target: Node) -> List[Node]:
    unvisited = nodes.copy()
    while unvisited:
        node = next_node(unvisited)
        if node == target:
            path = []
            while node.prev is not None:
                path.append(node.prev)
                node = node.prev
            return list(reversed(path))
        for neighbor in neighbors(y_x_nodes, node):
            distance = node.distance + neighbor.weight
            if distance < neighbor.distance:
                neighbor.distance = distance
                neighbor.prev = node
    return []


def main(input_file: str):
    y_x_nodes: List[List[Node]] = []
    nodes: List[Node] = []
    with open(input_file, 'r') as i:
        for y, line in enumerate(i):
            line = line.strip()
            if line == '':
                continue
            y_x_nodes.append([])
            for x, weight in enumerate(line):
                node = Node(x, y, int(weight))
                nodes.append(node)
                y_x_nodes[y].append(node)

    nodes[0].distance = 0

    print(shortest_path(y_x_nodes, nodes, nodes[-1]))


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'
    main(input_file)
