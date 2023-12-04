import re
from typing import Dict, List, Tuple
from queue import Queue

def part1(card_dict: Dict[int, Tuple[List[int], List[int]]]) -> int:
    matches = [len(set(card[0]) & set(card[1])) for card in card_dict.values()]
    return sum([2 ** (m - 1) if m > 1 else (1 if m == 1 else 0) for m in matches])

def part2(card_dict: Dict[int, Tuple[List[int], List[int]]]) -> int:
    card_count = 0
    match_dict = dict([(n, len(set(w) & set(y))) for n, (w, y) in card_dict.items()])
    # Init queue
    queue = Queue()
    for card_number in card_dict.keys():
        queue.put(card_number)
    # Simulate game rules without dynamic programming
    while not queue.empty():
        card_number = queue.get()
        card_count += 1
        matches = match_dict[card_number]
        for i in range(card_number + 1, card_number + match_dict[card_number] + 1):
            if i in card_dict:
                queue.put(i)
    return card_count

if __name__ == '__main__':
    card_dict = dict()  # {card_number: (winning_numbers, your_numbers)}
    with open('input/day_04.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            card_number_string, number_lists = line.split(': ')
            card_number = int(card_number_string.split(' ')[-1])
            winning_card, your_card = number_lists.split(' | ')
            winning_numbers = [int(n) for n in winning_card.split(' ') if n]
            your_numbers = [int(n) for n in your_card.split(' ') if n]
            card_dict[card_number] = (winning_numbers, your_numbers)
    
    # Start
    print(f'Part 1: {part1(card_dict)}')
    print(f'Part 2: {part2(card_dict)}')
