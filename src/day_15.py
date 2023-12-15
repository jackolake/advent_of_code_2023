from typing import List

def get_hash(text: str) -> int:
    value = 0
    for letter in text:
        value += ord(letter)
        value = (value * 17) % 256
    return value

def part1(input_list: List[str]) -> int:
    return sum([get_hash(token) for token in input_list])

if __name__ == '__main__':
    with open('input/day_15.txt', 'r') as f:
        input_list = list(f.read().strip().split(','))

    print(f'Part 1: {part1(input_list)}')