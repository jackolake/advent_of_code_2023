from typing import Dict

part1_lookup_dict = dict([(str(i), i) for i in range(10)])
part2_lookup_dict = dict(part1_lookup_dict, one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9)

def run(s: str, trans: Dict[str, int]) -> int:
    tokens = [trans[k] for i in range(len(s)) for k in trans.keys() if s[i:].startswith(k)]
    return tokens[0] * 10 + tokens[-1]

if __name__ == '__main__':
    with open('input/day_01.txt', 'r') as f:
        input_lines = [line.strip() for line in f.readlines()]
    
    print(f'Part 1: {sum([run(l, part1_lookup_dict) for l in input_lines])}')
    print(f'Part 2: {sum([run(l, part2_lookup_dict) for l in input_lines])}')