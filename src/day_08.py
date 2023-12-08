from typing import Dict, List, Tuple, Callable
import re
import math
from functools import reduce

def run(start_node: str, end_condition: Callable, move_pattern: str, path_map: Dict[str, Tuple[str, str]]) -> int:
    i = 0
    move_count = 0
    current_node = start_node
    while True:
        move = {'L': 0, 'R': 1}[move_pattern[i]]
        current_node = path_map[current_node][move]
        move_count += 1
        if end_condition(current_node):
            break
        i = (i + 1) % len(move_pattern)
    return move_count

def part1(move_pattern: str, path_map: Dict[str, Tuple[str, str]]) -> int:
   return run('AAA', lambda x: x == 'ZZZ', move_pattern, path_map)

def part2(move_pattern: str, path_map: Dict[str, Tuple[str, str]]) -> int:
    starting_nodes = [node for node in path_map.keys() if node.endswith('A')]
    results = [run(n, lambda x: x[-1] == 'Z', move_pattern, path_map) for n in starting_nodes]
    return reduce(lambda x, y: math.lcm(x, y), results)

if __name__ == '__main__':
    move_pattern = ''  # RL
    path_map = {}  # {source: (left, right)}
    with open('input/day_08.txt', 'r') as f:
        input_lines = [line.strip() for line in f.readlines() if line.strip()]
        move_pattern = input_lines[0]
        for l in input_lines[1:]:
            source, left, right = re.findall(r'\w+', l) # AAA = (BBB, CCC)
            path_map[source] = (left.strip(','), right)
    
    # Start
    print(f'Part 1: {part1(move_pattern, path_map)}')
    print(f'Part 2: {part2(move_pattern, path_map)}')
