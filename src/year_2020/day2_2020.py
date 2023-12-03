import re


def parse_password(line, policy_one=True) -> bool:
    matches = re.match(r'(\d+)-(\d+) (\w): (\w+)', line)

    min_count = int(matches[1])
    max_count = int(matches[2])
    match_letter = matches[3]
    password = matches[4]
    
    if policy_one:
        return min_count <= password.count(match_letter) <= max_count
    else:
        return (password[min_count-1]== match_letter) ^ (password[max_count-1] == match_letter) 


valid_1 = 0
valid_2 = 0
with open('inputs/day2_2020.txt') as f:
    for line in f.readlines():
        valid_1 += parse_password(line.strip())
        valid_2 += parse_password(line.strip(), policy_one=False)
print(valid_1)
print(valid_2)
