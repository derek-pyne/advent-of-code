import os
from collections import Counter
from functools import cmp_to_key

hands = []
with open(os.path.join(os.path.dirname(__file__), 'inputs/day_7.txt')) as f:
    for line in f.readlines():
        cards, bid = line.strip().split(' ')
        hands.append((cards, int(bid)))

def hand_rank(a):
    a_cnts = Counter(a)
    joker_count = a_cnts['J']
    if joker_count > 0:
        most_common_letter = a_cnts.most_common()[0][0] 
        if most_common_letter == 'J':
            if len(a_cnts) != 1:
                second_common_letter = a_cnts.most_common()[1][0] 
                a = a.replace('J', second_common_letter)
        elif most_common_letter != 'J':
            a = a.replace('J', a_cnts.most_common()[0][0])
        a_cnts = Counter(a)
    
    most_common = a_cnts.most_common()[0][1]
    second_most_common = a_cnts.most_common()[1][1] if len(a_cnts) >1 else 0
    
    rank = most_common
    
    if rank == 3 and second_most_common ==2:
        rank = 3.5
    elif rank == 2 and second_most_common ==2:
        rank = 2.5
        
    return rank


def compare_hands(a, b) -> int:
    if hand_rank(a) > hand_rank(b):
        return 1
    elif hand_rank(a) < hand_rank(b):
        return -1
    else:
        for a_char, b_char in zip(a, b):
            # card_rank = 'AKQJT98765432'
            card_rank = 'AKQT98765432J'
            if card_rank.index(a_char) < card_rank.index(b_char):
                return 1
            elif card_rank.index(a_char) > card_rank.index(b_char):
                return -1
    return 0
    
sorted_hands = sorted(hands, key=cmp_to_key(lambda a, b: compare_hands(a[0], b[0])))
print(hands)
print(sorted_hands)
winnings = 0
for i, (hand, bid) in enumerate(sorted_hands):
    winnings += (i+1) * bid
print(winnings)
