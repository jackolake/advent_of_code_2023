from typing import List, Optional
import pandas as pd

def roll(seq: str, forward: bool) -> str:  #  O.#O..# => .O#..O#
    results = []
    for segment in seq.split('#'):
        spaces, balls = ''.join(segment.count('.') * ['.']), ''.join(segment.count('O') * ['O'])
        results.append((spaces + balls) if forward else (balls + spaces))
    return '#'.join(results)

def calc_score(df: pd.DataFrame) -> int:
    result = df[::-1].reset_index(drop=True)  # Flip it to calc weight
    return ((result == 'O').sum(axis=1) * (result.index + 1)).sum()

def run(df: pd.DataFrame, roll_count: int) -> int:
    for i in range(roll_count):
        if i % 10000 == 0:
            print(i)
        # North, west, south, east
        if i % 4 == 0:  # North
            for col in df.columns:
                df[col] = list(roll(''.join(df[col].tolist()), forward=False))
        elif i % 4 == 1: # west
            for idx in df.index:
                df.loc[idx] = list(roll(''.join(df.loc[idx].tolist()), forward=False))
        elif i % 4 == 2: # South 
            for col in df.columns:
                df[col] = list(roll(''.join(df[col].tolist()), forward=True))
        else: # east
            for idx in df.index:
                df.loc[idx] = list(roll(''.join(df.loc[idx].tolist()), forward=True))
    return calc_score(df)

def part1(df: pd.DataFrame) -> int:
    return run(df, roll_count=1)

def part2(df: pd.DataFrame) -> int:
    return run(df, roll_count=1000000000)

if __name__ == '__main__':
    with open('input/day_14.txt', 'r') as f:
        df = pd.DataFrame([dict([(x, s) for x, s in enumerate(l.strip())]) for l in f.readlines()])
    print(f'Part 1: {part1(df)}')
    print(f'Part 2: {part2(df)}')