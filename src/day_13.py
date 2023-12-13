from typing import List, Optional
import pandas as pd


def find_horizontal_reflection(df: pd.DataFrame, error_count: int) -> Optional[int]:
    for mirror_idx in range(1, len(df.index)):
        df_up, df_down = df.loc[0:mirror_idx - 1][::-1].reset_index(drop=True), df.loc[mirror_idx:].reset_index(drop=True)
        row_size = min(len(df_up), len(df_down))
        df_up, df_down = df_up.loc[:row_size - 1], df_down.loc[:row_size - 1]
        if (df_up == df_down).sum().sum() + error_count == (row_size * len(df.columns)):
            return mirror_idx
    return None

def find_vertical_reflection(df: pd.DataFrame, error_count: int) -> Optional[int]:
    return find_horizontal_reflection(df.transpose(), error_count)

def run(input_list: List[pd.DataFrame], error_count: int) -> int:
    horiz_list = list(filter(None, [find_horizontal_reflection(i, error_count) for i in input_list]))
    vert_list = list(filter(None, [find_vertical_reflection(i, error_count) for i in input_list]))
    return sum([h * 100 for h in horiz_list]) + sum([v for v in vert_list])

def part1(input_list: List[pd.DataFrame]) -> int:
    return run(input_list, error_count = 0)

def part2(input_list: List[pd.DataFrame]) -> int:
    return run(input_list, error_count = 1)

if __name__ == '__main__':
    with open('input/day_13.txt', 'r') as f:
        input_list = [pd.DataFrame([dict([(x, s) for x, s in enumerate(l.strip())]) for l in pattern.splitlines()])
                      for pattern in f.read().split('\n\n')]

    print(f'Part 1: {part1(input_list)}')
    print(f'Part 2: {part2(input_list)}')