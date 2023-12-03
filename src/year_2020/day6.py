from dataclasses import dataclass

from typing import List


@dataclass
class Planet:
    name: str
    orbits: 'Planet' = None

    def orbit_chain(self) -> List[str]:
        next_planet = self
        oc = []
        while True:
            next_planet = next_planet.orbits
            if next_planet is None:
                break
            oc.append(next_planet.name)

        return oc


com = Planet(name='COM')
planets = {
    'COM': com
}
with open('inputs/day6.txt') as f:
    for line in f.readlines():
        base, orbit = line.strip().split(')')
        if base not in planets:
            base_planet = Planet(name=base)
            planets[base_planet.name] = base_planet
        else:
            base_planet = planets[base]
        if orbit not in planets:
            orbit_planet = Planet(name=orbit)
            planets[orbit_planet.name] = orbit_planet
        else:
            orbit_planet = planets[orbit]

        orbit_planet.orbits = base_planet

print(sum([len(p.orbit_chain()) for p in planets.values()]))

you = planets['YOU'].orbits
san = planets['SAN'].orbits

print(you.name)
you_chain = you.orbit_chain()
print(you_chain)
san_chain = san.orbit_chain()
print(san_chain)

for link in you_chain:
    if link in san_chain:
        connection = link
        break
print(f'Connection: {connection}')
you_dist = you_chain.index(connection) + 1
san_dist = san_chain.index(connection) + 1
print(you_dist, san_dist, you_dist + san_dist)
