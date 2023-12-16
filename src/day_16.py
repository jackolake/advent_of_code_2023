from queue import Queue
from typing import List, Tuple
import pandas as pd

SYM_DICT = {
    # {in_direction: tuples of out directions}
    '|': {(1, 0): ((0, 1), (0, -1)),
          (-1, 0): ((0, 1), (0, -1))},
    '-': {(0, 1): ((-1, 0), (1, 0)),
          (0, -1): ((-1, 0), (1, 0))},
    '\\': {
        (1, 0): ((0, 1), ),
        (-1, 0): ((0, -1), ),
        (0, 1): ((1, 0), ),
        (0, -1): ((-1, 0), )
    },
    '/': {
        (1, 0): ((0, -1), ),
        (-1, 0): ((0, 1), ),
        (0, 1): ((-1, 0), ),
        (0, -1): ((1, 0), )
    },
}


def run(df: pd.DataFrame, current_pos: Tuple[int, int], current_direction: Tuple[int, int]):
    max_x, max_y = len(df.columns), len(df.index)
    energy_df = pd.DataFrame(dict([(x, 0) for x in range(max_x)]) for y in range(max_y))
    q = Queue()
    q.put((current_pos, current_direction))
    history = set()
    while not q.empty():
        (x, y), current_direction = q.get()
        energy_df.at[y, x] = 1  # Light it up
        next_directions = SYM_DICT.get(df.at[y, x], {}).get(current_direction, tuple()) or (current_direction, )
        for next_direction in next_directions:
            next_x, next_y = x + next_direction[0], y + next_direction[1]
            if 0 <= next_x < max_x and 0 <= next_y < max_y and (next_x, next_y, next_direction) not in history:
                history.add((x, y, current_direction))
                q.put(((next_x, next_y), next_direction))
    return energy_df.sum().sum()

def part1(df: pd.DataFrame) -> int:
    return run(df, current_pos=(0, 0), current_direction=(1, 0))
    
def part2(df: pd.DataFrame) -> int:
    max_x, max_y = len(df.columns), len(df.index)
    left_to_right = max([run(df, (0, y), (1, 0)) for y in range(max_y)])
    right_to_left = max([run(df, (max_x - 1, y), (-1, 0)) for y in range(max_y)])
    top_to_bottom = max([run(df, (x, 0), (0, 1)) for x in range(max_x)])
    bottom_to_top = max([run(df, (x, max_y - 1), (0, -1)) for x in range(max_x)])
    return max([left_to_right, right_to_left, top_to_bottom, bottom_to_top])
    

if __name__ == '__main__':
    with open('input/day_16.txt', 'r') as f:
        df = pd.DataFrame([dict([(x, s) for x, s in enumerate(l.strip())]) for l in f.readlines()])

    print(f'Part 1: {part1(df)}')
    print(f'Part 2: {part2(df)}')