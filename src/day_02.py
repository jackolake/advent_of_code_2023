from functools import reduce
from typing import Dict, List, Tuple


def part1(instructions: List[Tuple[int, Dict[str, int]]]) -> int:
    elf_cubes = {'red': 12, 'green': 13, 'blue': 14}       
    return sum([game_num for game_num, rounds in instructions
                if all([all([(elf_cubes[colour] >= cube) for colour, cube in r.items()]) for r in rounds])])

def part2(instructions: List[Tuple[int, Dict[str, int]]]) -> int:
    value = 0
    for game_num, rounds in instructions:
        cube_dict = dict([(c, max([r.get(c, 0) for r in rounds])) for c in ['red', 'green', 'blue']])
        value += reduce(lambda x, y: x * y, [v for v in cube_dict.values() if v > 0])
    return value

if __name__ == '__main__':
    instructions = []  # (game#, List[Dict[str, int]])
    with open('input/day_02.txt', 'r') as f:
        for line in f.readlines():
            game_strings, inst_strings = line.strip().split(': ')
            game_num = int(game_strings.split(' ')[-1])
            rounds = []
            for game_round in inst_strings.split('; '):
                rounds.append(dict([(cube_setting.split(' ')[1], int(cube_setting.split(' ')[0])) for cube_setting in game_round.split(', ')]))
            instructions.append((game_num, rounds))

    # Start
    print(f'Part 1: {part1(instructions)}')
    print(f'Part 2: {part2(instructions)}')
