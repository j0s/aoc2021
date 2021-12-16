#!/bin/env python

from typing import List, Dict, Set
import sys


def search_graph(
    graph: Dict[str, List[str]],
    from_node: str,
    visited_small_cave_twice: bool = False,
    visited: Set[str] = set()
) -> List[List[str]]:
    paths = []
    visited.add(from_node)
    for neighbor in graph[from_node]:
        if (neighbor.islower() and neighbor != 'start'
                and neighbor in visited):
            if not visited_small_cave_twice:
                for path in search_graph(graph, neighbor, True,
                                         visited.copy()):
                    paths.append([from_node] + path)
            continue
        elif neighbor == 'start':
            continue
        elif neighbor == 'end':
            paths.append([from_node, 'end'])
        else:
            for path in search_graph(graph, neighbor, visited_small_cave_twice,
                                     visited.copy()):
                paths.append([from_node] + path)

    return paths


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest

        doctest.testmod()
        sys.exit(0)

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input'

    graph: Dict[str, List[str]] = {}
    with open(input_file, 'r') as i:
        for line in i:
            line = line.strip()
            if line == '':
                continue
            start, end = line.split('-')
            if start not in graph:
                graph[start] = []
            graph[start].append(end)
            if end not in graph:
                graph[end] = []
            graph[end].append(start)

    all_paths = search_graph(graph, 'start')
    print(f'paths: {len(all_paths)}')
