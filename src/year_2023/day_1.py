import os


def get_first_num(line):
    buff = ''
    for c in line:
        buff += c
        for k, v in nums.items():
            if k in buff:
                return v
            
def get_second_num(line):
    buff = ''
    for c in line[::-1]:
        buff = c + buff
        for k, v in nums.items():
            if k in buff:
                return v


with open(os.path.join(os.path.dirname(__file__), 'inputs/day_1.txt')) as f:
    big_sum = 0
    for line in f.readlines():
        nums = {
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
        }
        line = line.strip()
        print(line)
        first_num = get_first_num(line)
        second_num = get_second_num(line)
        num = int(f'{first_num}{second_num}') 
        big_sum += num
        print(f'Line: {line}, first_num: {first_num}, second_num: {second_num}')
    print(f'The sum is {big_sum}')
