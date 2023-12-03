import re
from typing import Dict, List, Tuple

ADJ_LIST = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

def part1(parts_map: Dict[Tuple[Tuple[int, int], int], str]) -> int:
    value = 0
    # For each part number, check if any symbol is nearby
    symbol_coordinates_set = set([(x, y) for ((x, _), y), symbol in parts_map.items() if not symbol.isnumeric()])
    for ((x_start, x_end), y), token in parts_map.items():
        if token.isnumeric():  
            nearby_coordinates = [(x + adj_x, y + adj_y) for x in range(x_start, x_end) for (adj_x, adj_y) in ADJ_LIST]
            if set(nearby_coordinates) & symbol_coordinates_set:
                value += int(token)
    return value

def part2(parts_map: Dict[Tuple[Tuple[int, int], int], str]) -> int:
    value = 0
    gear_coordinates_set = [(x, y) for ((x, _), y), symbol in parts_map.items() if symbol == '*']
    parts = dict([(((xs, xe), y), int(token)) for ((xs, xe), y), token in parts_map.items() if token.isnumeric()])
    # For each gear, find the nearby parts indexed by (x_start, y)
    for gear_x, gear_y in gear_coordinates_set:
        nearby_coordinates = [(gear_x + adj_x, gear_y + adj_y) for (adj_x, adj_y) in ADJ_LIST]
        nearby_parts = list(set([((xs, y), part_number) for ((xs, xe), y), part_number in parts.items()
                                for x in range(xs, xe) if (x, y) in nearby_coordinates]))
        if len(nearby_parts) == 2:
            value += nearby_parts[0][1] * nearby_parts[1][1]
    return value

if __name__ == '__main__':
    parts_map = dict()  # {((x_start, x_end), y): part_or_symbol}
    with open('input/day_03.txt', 'r') as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for match in re.finditer(r'(\d+|[^\.])', line):
                parts_map[((match.span()), y)] = match.group()            
    
    # Start
    print(f'Part 1: {part1(parts_map)}')
    print(f'Part 2: {part2(parts_map)}')
