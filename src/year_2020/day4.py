
pass_range = [278384,824795]


def is_valid(num):
    str_num = str(num)
    
    prev_digit = '0'
    for digit in str_num:
        if prev_digit > digit:
            return False
        prev_digit = digit
    
    groups = [str_num.count(ch) for ch in set(str_num)]
    for g in groups:
        if g == 2:
            return True
    return False

print(is_valid(112233), True)
print(is_valid(123444), False)
print(is_valid(111122), True)
print(is_valid(125555), True)
print(is_valid(125557), False)
print(is_valid(111111), False)
# 
valid_count = 0
for num in range(pass_range[0], pass_range[1]+1):
    valid_count += is_valid(num)
print(f'Valid count: {valid_count}')
