import os
import re



def predict_next(xs):
    D = []
    for i in range(len(xs)-1):
        D.append(xs[i+1] - xs[i])
    if all(y == 0 for y in D):
        return xs[0]
    else:
        # return xs[-1] + predict_next(D)
        return xs[0] - predict_next(D)

with open(os.path.join(os.path.dirname(__file__), 'inputs/day_9.txt')) as f:
    ans = 0
    for line in f.readlines():
        xs = [int(x) for x in line.split()]
        next_num = predict_next(xs)
        ans += next_num

print(ans)
