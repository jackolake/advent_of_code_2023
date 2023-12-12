from typing import List, Dict, Tuple
from functools import cache

@cache
def run(seq: str, cluster: Tuple[int]) -> int:
    # Termination: Good if no onsen left and no pending cluster
    if not seq:
        return 1 if not cluster else 0
    elif not cluster:
        return 1 if '#' not in seq else 0
    value = 0
    if seq[0] in ('.', '?'):            # 1) .### => ###  2) ?### => .### => ###
        value += run(seq[1:], cluster)  # treat leftmost as processed and count the rest
    if seq[0] in ('#', '?'):                                          # 3) #### / ?### => try to match current cluster target
        target_count = cluster[0]
        substring = seq[:target_count]
        if len(substring) == target_count and '.' not in substring:  
            if len(seq) == target_count or seq[target_count] != '#':  # Also the onsen after this is not broken (i.e. not #####)
                value += run(seq[target_count + 1:], cluster[1:])     # matched a cluster, move to the next cluster
    return value


def part1(input_list: Tuple[Tuple[str, Tuple[int]]]) -> int:
    return sum([run(seq, cluster) for seq, cluster in input_list])

def part2(input_list: Tuple[Tuple[str, Tuple[int]]]) -> int:
    # "replace the list of spring conditions with five copies of itself (separated by ?)" (I missed the "?" initially)
    return part1([('?'.join([seq] * 5), cluster * 5) for seq, cluster in input_list])

if __name__ == '__main__':
    input_list = []  # (sequence, cluster)   e.g. [('?###????????', [3,2,1])]
    with open('input/day_12.txt', 'r') as f:
        for line in f.readlines():
            seq, cluster = line.strip().split(' ')
            input_list.append((seq, tuple([int(n) for n in cluster.split(',')])))
            
    print(f'Part 1: {part1(input_list)}')
    print(f'Part 2: {part2(input_list)}')