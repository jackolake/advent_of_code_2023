from typing import List, Dict, Tuple
from itertools import product
import re

def check(onsen_list: str, group_sizes: List[int]) -> bool:
    return [len(p) for p in re.findall('#+', onsen_list)] == group_sizes

def gen_combinations(input_text: str) -> List[str]:
    replace_count = input_text.count('?')
    replacements = list([''.join(p) for p in product(['.', '#'], repeat=replace_count)])
    replace_indices = [i for i, s in enumerate(input_text) if s == '?']
    return [''.join([replacement[replace_indices.index(i)] if i in replace_indices else input_text[i]
                     for i in range(len(input_text))])
                     for replacement in replacements]

def part1(onsen_group_list: List[str], good_onsen_size_list: List[List[int]]) -> int:
    return sum([len([g for g in gen_combinations(onsen_group) if check(g, group_sizes)])
                for onsen_group, group_sizes in zip(onsen_group_list, good_onsen_size_list)])

def part2(onsen_group_list: List[str], good_onsen_size_list: List[List[int]]) -> int:
    onsen_group_list = [(l * 5) for l in onsen_group_list]
    good_onsen_size_list = [(l * 5) for l in good_onsen_size_list]
    return part1(onsen_group_list, good_onsen_size_list)


if __name__ == '__main__':
    onsen_sequence_list = []
    good_onsen_size_list = []
    with open('input/day_12.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        for line in lines:
            symbol_list, number_list = line.split(' ') # '#.#.### 1,1,3'
            onsen_sequence_list.append(symbol_list)
            good_onsen_size_list.append([int(n) for n in number_list.split(',')])
    print(f'Part 1: {part1(onsen_sequence_list, good_onsen_size_list)}')
    print(f'Part 2: {part2(onsen_sequence_list, good_onsen_size_list)}')