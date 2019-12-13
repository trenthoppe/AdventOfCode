# Read input and initialize globals
file = open("test.txt", "r")
orbits = list(map(lambda o: o.split(')'), file.read().splitlines()))
orbitters = []

# Orbitter class to keep track of self in relation to other orbitters
class Orbitter:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.indirectOrbits = parent.indirectOrbits + 1 if not parent is None else 0 

# Lmao this would be useful if our center of mass wasn't labeled COM 
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

# Gets an orbitter by name
def findOrbitterByName(name):
    return [orbitter for orbitter in orbitters if orbitter.name == name][0]

# Recursively get all parents for a specific orbitter
def getParents(orbitter):
    parent = orbitter.parent
    if parent is None:
        return []
    return [parent] + getParents(parent)

# Gets the closest parent to two orbitters
def findClosestCommonParent(orbitter1, orbitter2):
    orbitter1Parents = getParents(orbitter1)
    orbitter2Parents = getParents(orbitter2)
    # Return at the first one we find because that 
    # one is the closest
    for orbitter1Parent in orbitter1Parents:
        for orbitter2Parent in orbitter2Parents:
            if orbitter1Parent == orbitter2Parent:
                return orbitter1Parent

# Gets minimum orbital transfers for two orbitters
def findMinimumOrbitalTransfers(orbitter1, orbitter2):
    closestCommonParent = findClosestCommonParent(orbitter1, orbitter2)
    # Subtract 1 because we don't count the distance of the orbitter you are stuck on
    orbitter1DistanceToParent = orbitter1.indirectOrbits - closestCommonParent.indirectOrbits - 1
    orbitter2DistanceToParent = orbitter2.indirectOrbits - closestCommonParent.indirectOrbits -1
    # The minimum orbital transfer is the number of indirect orbits it takes 
    # to get to the closest common parent
    return orbitter1DistanceToParent + orbitter2DistanceToParent

# Find com even if it isn't labeled "COM"
com = findCOM(orbits)
# Build solarsystem and count orbits
buildSolarSystem(com, None)
print(countOrbitsInSolarSystem())

# Find the orbitters that you and santa are stuck on 
# and calculate minimum orbital transfer
you = findOrbitterByName("YOU")
santa = findOrbitterByName("SAN")
print(findMinimumOrbitalTransfers(you, santa))