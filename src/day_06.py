from functools import reduce
from typing import Dict, List, Tuple
import re

def part1(time_list: List[int], distance_list: List[int]) -> int:
    results = [sum([1 for v in range(1, t) if v * (t - v) > d]) for t, d in zip(time_list, distance_list)]
    return reduce(lambda x, y: x * y, results)

def part2(time_list: List[int], distance_list: List[int]) -> int:
    return part1([int(''.join([str(t) for t in time_list]))],
                 [int(''.join([str(t) for t in distance_list]))])

if __name__ == '__main__':
    with open('input/day_06.txt', 'r') as f:
        time_list, distance_list = [[int(n) for n in re.findall(r'\d+', l.strip())] for l in f.readlines()]

    # Start
    print(f'Part 1: {part1(time_list, distance_list)}')
    print(f'Part 2: {part2(time_list, distance_list)}')
