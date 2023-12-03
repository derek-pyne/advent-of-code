with open('../year_2020/inputs/data.txt') as f:
    wires = [x.strip().split(',') for x in f.readlines()]

print(wires)

wire_locations = []


def get_wire_visits(wire):
    visits = set()
    visit_steps = {}
    loc = [0, 0]
    steps_taken = 0
    for p in wire:
        direction = p[0]
        steps = int(p[1:])
        print(direction, steps)
        if direction == 'U':
            for _ in range(steps):
                steps_taken += 1
                loc[1] += 1
                if tuple(loc) not in visits:
                    visits.add(tuple(loc))
                    visit_steps[tuple(loc)] = steps_taken
        elif direction == 'D':
            for _ in range(steps):
                steps_taken += 1
                loc[1] -= 1
                if tuple(loc) not in visits:
                    visits.add(tuple(loc))
                    visit_steps[tuple(loc)] = steps_taken
        elif direction == 'R':
            for _ in range(steps):
                steps_taken += 1
                loc[0] += 1
                if tuple(loc) not in visits:
                    visits.add(tuple(loc))
                    visit_steps[tuple(loc)] = steps_taken
        elif direction == 'L':
            for _ in range(steps):
                steps_taken += 1
                loc[0] -= 1
                if tuple(loc) not in visits:
                    visits.add(tuple(loc))
                    visit_steps[tuple(loc)] = steps_taken
    return visit_steps


w1 = get_wire_visits(wires[0])
w2 = get_wire_visits(wires[1])

crosses = set(w1.keys()).intersection(set(w2.keys()))
# dists = [abs(x) + abs(y) for x, y in crosses]
dists = [w1[c] + w2[c] for c in crosses]
    
print(f'Min_dist: {min(dists)}')
