

with open('day2.txt') as f:
    readings = f.readlines()

counts = []
for reading in readings:
    reading = reading.strip()

    for i, bit in enumerate(reading):
        if i >= len(counts):
            counts.append({})

        if bit not in counts[i]:
            counts[i][bit] = 0

        counts[i][bit] += 1

epsilon = ''
gamma = ''
for position in counts:
    if position['1'] < position['0']:
        epsilon += '1'
        gamma += '0'
    else:
        gamma += '1'
        epsilon += '0'

epsilon_val = int(epsilon, 2)
gamma_val = int(gamma, 2)
print(epsilon, epsilon_val, gamma, gamma_val, epsilon_val*gamma_val)

