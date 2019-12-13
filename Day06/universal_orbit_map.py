# Read input and initialize globals
file = open("input.txt", "r")
orbits = list(map(lambda o: o.split(')'), file.read().splitlines()))
orbitters = []

# Orbitter class to keep track of self in relation to other orbitters
class Orbitter:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.indirectOrbits = parent.indirectOrbits + 1 if not parent is None else 0 

# This would be useful if our center of mass wasn't labeled COM lol
def findCOM(orbits):
    orbitted = set([orbit[0] for orbit in orbits])
    orbitters = set([orbit[1] for orbit in orbits])
    return list(orbitted.difference(orbitters))[0]

# Recursively build our solarsystem from the inside out
def buildSolarSystem(child, parent):
    orbitter = Orbitter(child, parent)
    orbitter.children = findChildOrbitters(orbitter)
    orbitters.append(orbitter)

    for child in orbitter.children:
        buildSolarSystem(child, orbitter)

# Find the children of a parent orbitter
def findChildOrbitters(orbitter):
    return [orbit[1] for orbit in orbits if orbit[0] == orbitter.name]

# Sum up all indirect orbits for all orbitters
def countOrbitsInSolarSystem():
    return sum(orbitter.indirectOrbits for orbitter in orbitters)

# Find com even if it isn't labeled "COM"
com = findCOM(orbits)
# Build solarsystem and count orbits
buildSolarSystem(com, None)
print(countOrbitsInSolarSystem())