f_path = '2020/inputs/day1.txt'

nums = []
with open(f_path) as f:
    for line in f:
        nums.append(int(line))

target = 2020


def get_sum_nums(nums, target):
    for num in nums:
        desired = target - num
        if desired in nums:
            return num, desired

    return None, None


num, desired = get_sum_nums(nums, target=2020)
print(f'Num 1:{num} num 2: {desired} multiply {num * desired}')

for num in nums:
    other_nums = nums.copy()
    other_nums.remove(num)
    num2, num3 = get_sum_nums(other_nums, target=2020 - num)
    if num2 is not None:
        print(f'num: {num}, num2: {num2}, num3: {num3}, multiple: {num * num2 * num3}')
        break
