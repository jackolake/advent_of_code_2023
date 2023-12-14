from typing import List, Optional
import pandas as pd

def roll(seq: str, forward: bool) -> str:  #  O.#O..# => .O#..O#
    return '#'.join([((s.count('.') * '.') + (s.count('O') * 'O')) if forward else 
                     ((s.count('O') * 'O') + (s.count('.') * '.')) for s in seq.split('#') ])

def calc_score(df: pd.DataFrame) -> int:
    result = df[::-1].reset_index(drop=True)  # Flip it to calc weight
    return ((result == 'O').sum(axis=1) * (result.index + 1)).sum()

def run_cycles(df: pd.DataFrame, cycle_count: int) -> int:
    for _ in range(cycle_count):
        for col in df.columns: 
            df[col] = list(roll(''.join(df[col]), forward=False))          # North
        for idx in df.index:
            df.loc[idx] = list(roll(''.join(df.loc[idx]), forward=False))  # West
        for col in df.columns: 
            df[col] = list(roll(''.join(df[col]), forward=True))           # South
        for idx in df.index:
            df.loc[idx] = list(roll(''.join(df.loc[idx]), forward=True))   # East
    return calc_score(df)

def part1(df: pd.DataFrame) -> int:
    for col in df.columns: 
        df[col] = list(roll(''.join(df[col]), forward=False))
    return calc_score(df)

def part2(df: pd.DataFrame) -> int:
    return run_cycles(df, cycle_count=1000000000)

if __name__ == '__main__':
    with open('input/day_14.txt', 'r') as f:
        df = pd.DataFrame([dict([(x, s) for x, s in enumerate(l.strip())]) for l in f.readlines()])
    print(f'Part 1: {part1(df)}')
    print(f'Part 2: {part2(df)}')