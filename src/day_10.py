from typing import List, Dict, Tuple
from queue import Queue
import pandas as pd  # Just for an easier way to visualize e.g., print(symbol_df)

PIPE_DICT = {
    '-': set([(-1, 0), (1, 0)]),
    '|': set([(0, -1), (0, 1)]),
    'L': set([(1, 0), (0, -1)]),
    'F': set([(1, 0), (0, 1)]),
    'J': set([(0, -1), (-1, 0)]),
    '7': set([(-1, 0), (0, 1)]),
}

def run_bfs(start_pos: Tuple[int, int], symbol_df: pd.DataFrame) -> Dict[Tuple[int, int], int]:
    max_x, max_y = len(symbol_df.columns), len(symbol_df.index)
    distance_df = pd.DataFrame([dict([(x, 0 if (x, y) == start_pos else pd.NA) for x in range(max_x)]) for y in range(max_y)])
    queue = Queue()
    queue.put(start_pos)
    while not queue.empty():
        x, y = queue.get()
        symbol = symbol_df.at[y, x]
        if symbol not in PIPE_DICT.keys():
            continue
        for (adj_x, adj_y) in PIPE_DICT[symbol]:
            neighbour_x, neighbour_y = x + adj_x, y + adj_y
            if 0 <= neighbour_x < max_x and 0 <= neighbour_y < max_y and pd.isna(distance_df.at[neighbour_y, neighbour_x]):
                distance_df.at[neighbour_y, neighbour_x] = distance_df.at[y, x] + 1
                queue.put((neighbour_x, neighbour_y))
    return distance_df

def part1(start_pos: Tuple[int, int], symbol_df: pd.DataFrame) -> int:
    return run_bfs(start_pos, symbol_df).max().max()

def transition_count(other_tiles: List[str]) -> int:
    return sum([other_tiles.count(s) for s in ['J', '|', 'L']])  # pipe and 1 of the turning point pairs

def part2(start_pos: Tuple[int, int], symbol_df: pd.DataFrame) -> int:
    distance_df = run_bfs(start_pos, symbol_df)
    loop_df = symbol_df.copy()
    loop_df[distance_df.isna()] = pd.NA
    loop_df = loop_df.fillna(' ')
    max_y, max_x = len(loop_df.index), len(loop_df.columns)
    for y in range(max_y):
        for x in range(max_x):
            if loop_df.at[y, x] == ' ':
                left = list(reversed(loop_df.loc[y, 0:x-1].tolist()))
                right = loop_df.loc[y, x:max_x].tolist()
                if all([(transition_count(test) % 2 == 1) for test in [left, right]]):
                    loop_df.at[y, x] = 'I'
    return loop_df.eq('I').sum().sum()  # Number of "I"


if __name__ == '__main__':
    with open('input/day_10.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        max_x, max_y = len(lines[0]), len(lines)
    # Parse input into a pandas dataframe for visualization
    symbol_df = pd.DataFrame([dict([(x, symbol) for x, symbol in enumerate(line)]) for y, line in enumerate(lines)])
    # Get starting position
    start_y, start_x = symbol_df.where(symbol_df == "S").stack().index.tolist()[0]
    # Derive the actual symbol of starting position
    max_x, max_y = len(symbol_df.columns), len(symbol_df.index)
    starting_connections = set()
    for (adj_x, adj_y) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = start_x + adj_x, start_y + adj_y
        if 0 <= x < max_x and 0 <= y < max_y:
            if (adj_x * -1, adj_y * -1) in PIPE_DICT.get(symbol_df.at[y, x], (0, 0)):
                starting_connections.add((adj_x, adj_y))
    starting_symbol = [symbol for symbol, connections in PIPE_DICT.items() if starting_connections == connections][0]
    start_pos = (start_x, start_y)
    symbol_df.at[(start_y, start_x)] = starting_symbol

    # Real Start
    print(f'Part 1: {part1(start_pos, symbol_df)}')
    print(f'Part 2: {part2(start_pos, symbol_df)}')
