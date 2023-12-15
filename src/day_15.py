from collections import defaultdict
from typing import List
import re

def get_hash(text: str) -> int:
    value = 0
    for letter in text:
        value += ord(letter)
        value = (value * 17) % 256
    return value

def part1(input_list: List[str]) -> int:
    return sum([get_hash(token) for token in input_list])

def part2(input_list: List[str]) -> int:
    box_dict = defaultdict(dict)
    for instruction in input_list:
        label, op, focus_power = re.findall(r'(\w+)(=|-)(\d?)', instruction)[0]
        box_number = get_hash(label)
        if op == '-' and label in box_dict[box_number]:
            box_dict[box_number].pop(label)
        elif op == '=':
            box_dict[box_number][label] = int(focus_power)
    # Calc power
    return sum([(box_idx + 1) * sum([(slot_idx + 1) * focal_length for slot_idx, focal_length in enumerate(box.values())])
                for box_idx, box in box_dict.items()])


if __name__ == '__main__':
    with open('input/day_15.txt', 'r') as f:
        input_list = list(f.read().strip().split(','))

    print(f'Part 1: {part1(input_list)}')
    print(f'Part 2: {part2(input_list)}')