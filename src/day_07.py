from typing import Dict, List, Tuple, Callable
import pandas as pd

SCORE_MAP_PART1 = dict(dict([(str(i), i + 1) for i in range(2, 10)]),
                      **dict(T=11, J=12, Q=13, K=14, A=15))
SCORE_MAP_PART2 = dict(SCORE_MAP_PART1, J=2)
rule_map = {
    '5 of a kind': 6,
    '4 of a kind': 5,
    'Full House': 4,
    '3 of a kind': 3,
    'Two pair': 2,
    'One pair': 1,
    'High card': 0,
}

def get_hand_score_base(hand: str) -> Tuple[str, float]:
    card_occurence_dict = dict([(card, hand.count(card)) for card in set(hand)])
    base_multipler = 1000000
    max_occurence_count = max(card_occurence_dict.values())
    if max_occurence_count > 1:
        if sorted(card_occurence_dict.values(), reverse=True)[:2] == [3, 2]:
            reason = 'Full House'
        elif len([c for c in card_occurence_dict.values() if c == 2]) == 2:
            reason = 'Two pair'
        else:
            reason = 'One pair' if max_occurence_count == 2 else f'{max_occurence_count} of a kind'
    else:
        reason = 'High card'
    return reason, rule_map[reason] * 1000000

def get_hand_score_part1(hand: str, card_score_map: Dict[str, int]) -> Tuple[str, float]:
    reason, score = get_hand_score_base(hand)
    return reason, score + sum([card_score_map[card] * (100 ** (-i)) for i, card in enumerate(hand)])


def get_hand_score_part2(hand: str, card_score_map: Dict[str, int]) -> Tuple[str, float]:
    results = []
    reason, score = get_hand_score_base(hand)
    # Try all possible hands with the same tie-breaking score as J only determines rule type
    tie_breaker_score = sum([card_score_map[card] * (100 ** (-i)) for i, card in enumerate(hand)])
    possible_hands = set([hand] + ([hand.replace('J', card) for card in set(hand)] if 'J' in hand else []))
    for h in possible_hands:
        try_reason, try_score = get_hand_score_base(h)
        results.append((try_reason, try_score + tie_breaker_score))
    return sorted(results, key=lambda x: x[-1])[-1]
    

def run(hands_and_bets: List[Tuple[str, int]], scoring_func: Callable, card_score_map: Dict[str, int]) -> int:
    results = []
    for hand, bet in hands_and_bets:
        reason, score = scoring_func(hand, card_score_map)
        results.append({'hand': hand, 'bet': bet, 'score': score, 'reason': reason,})
    df = pd.DataFrame(results)
    df = df.sort_values(by='score').reset_index()
    df['rank'] = df.index + 1
    return sum(df['rank'] * df['bet'])

def part1(hands_and_bets: List[Tuple[str, int]]) -> int:
    return run(hands_and_bets, get_hand_score_part1, SCORE_MAP_PART1)

def part2(hands_and_bets: List[Tuple[str, int]]) -> int:
    return run(hands_and_bets, get_hand_score_part2, SCORE_MAP_PART2)


if __name__ == '__main__':
    hands_and_bets = []  # [(hand, bet)]
    with open('input/day_07.txt', 'r') as f:
        for line in f.readlines():
            hand, bet = line.strip().split(' ')
            hands_and_bets.append((hand, int(bet)))

    # Start
    print(f'Part 1: {part1(hands_and_bets)}')
    print(f'Part 2: {part2(hands_and_bets)}')
