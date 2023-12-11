from typing import List, Dict, Tuple
from itertools import combinations
import pandas as pd

def run(input_galaxies: List[Tuple[int, int]], expansion_pace: int) -> int:    
    empty_columns = [x for x in range(max_x) if set(input_df.loc[:, x].tolist()) == set(['.'])]
    empty_rows = [y for y in range(max_y) if set(input_df.loc[y, :].tolist()) == set(['.'])]
    return sum([abs(x1-x2) + abs(y1-y2)
                + sum([(expansion_pace - 1) for y in empty_rows if min(y1, y2) <= y <= max(y1, y2)])    # minus 1 because abs(y1-y2) counted the empty row once
                + sum([(expansion_pace - 1) for x in empty_columns if min(x1, x2) <= x <= max(x1, x2)]) # minus 1 because abs(x1-x2) counted the empty col once
                for (x1, y1), (x2, y2) in combinations(input_galaxies, 2)])

def part1(input_galaxies: List[Tuple[int, int]]) -> int:
    return run(input_galaxies, expansion_pace=2)
        
def part2(input_galaxies: List[Tuple[int, int]]) -> int:
    return run(input_galaxies, expansion_pace=1000000)


if __name__ == '__main__':
    with open('input/day_11.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        max_x, max_y = len(lines[0]), len(lines)
        input_df = pd.DataFrame([dict([(x, lines[y][x]) for x in range(max_x)]) for y in range(max_y)])

    input_galaxies = [(x, y) for (y, x) in input_df.where(input_df == "#").stack().index.tolist()]
    print(f'Part 1: {part1(input_galaxies)}')
    print(f'Part 2: {part2(input_galaxies)}')