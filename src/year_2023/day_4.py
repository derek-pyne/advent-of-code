import os
import re


def extract_numbers(string):
    return re.findall(r'\d+', string)

score = 0
winners = []
cards = 0
with open(os.path.join(os.path.dirname(__file__), 'inputs/day_4.txt')) as f:
    for line_num, line in enumerate(f.readlines()):
        left, right = line.split(':')[1].split('|')
        left_num = set(extract_numbers(left))
        right_num = set(extract_numbers(right))
        common_nums = left_num.intersection(right_num)
        
        # Part 1
        line_score = 0 if len(common_nums) == 0 else 2 ** (len(common_nums) - 1)
        score += line_score
        
        # Part 2
        current_winners = 0 if len(winners) == 0 else winners.pop(0)
        common_cnt = len(common_nums)
        # cards += 1
        # print(f'Line: {line_num+1}, Common cnt: {common_cnt} current winners: {current_winners}')
        for _ in range((1+current_winners)):
            cards +=1
            for i in range(common_cnt):
                if len(winners) > i:
                    winners[i] += 1
                else:
                    winners.append(1)
        
        
print(f'Total score: {score}')
print(f'Total cards: {cards}')
        
