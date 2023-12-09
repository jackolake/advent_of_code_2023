from typing import List

def extrapolate(history: List[int]) -> int:
    sequences = [history]
    while any([(n != 0) for n in sequences[-1]]):
        sequences.append([sequences[-1][i + 1] - sequences[-1][i] for i in range(len(sequences[-1]) - 1)])
    return sum([s[-1] for s in sequences])

def part1(history_list: List[List[int]]) -> int:
   return sum([extrapolate(history) for history in history_list])


def part2(history_list: List[List[int]]) -> int:
   return part1([list(reversed(h)) for h in history_list])


if __name__ == '__main__':
    history_list = []   # [[0, 3, 6, 9, 12, 15], ... ]
    with open('input/day_09.txt', 'r') as f:
        history_list = [[int(n) for n in l.strip().split(' ')] for l in f.readlines() if l.strip()]
    
    # Start
    print(f'Part 1: {part1(history_list)}')
    print(f'Part 2: {part2(history_list)}')
