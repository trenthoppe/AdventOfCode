# Read input and get wire paths
file = open("input.txt", "r")
# splitlines() to remove newline characters
lines = file.read().splitlines()
path1Instructions = lines[0].split(',')
path2Instructions = lines[1].split(',')

def traceInstruction(path, coord, distance, isPosIncrement):
    step = 0
    lastCoord = path[-1:][0][0]
    x = lastCoord[0]
    y = lastCoord[1]
    totalSteps = path[-1:][0][1]

    while step < distance:
        totalSteps += 1
        if coord == 'x':
            x = x + 1 if isPosIncrement else x - 1
            path.append(((x,y),totalSteps))
        elif coord == 'y':
            y = y + 1 if isPosIncrement else y - 1
            path.append(((x,y),totalSteps))
        step += 1

def tracePath(instructions):
    path = [((0,0),0)]

    for instruction in instructions:
        direction = instruction[0]
        distance = int(instruction[1:])
        if direction == 'U':
            traceInstruction(path, 'y', distance, True)
        elif direction == 'R':
            traceInstruction(path, 'x', distance, True)
        elif direction == 'D':
            traceInstruction(path, 'y', distance, False)
        elif direction == 'L':
            traceInstruction(path, 'x', distance, False)
        else:
            print("Direction not recognized")
    # Origin doesn't count as an intersection so just remove it
    path.remove(((0,0),0))
    return path

def findIntersections(path1, path2):
    path1Coords = set(coord[0] for coord in path1)
    path2Coords = set(coord[0] for coord in path2)
    return list(path1Coords.intersection(path2Coords))

def findManhattenDistance(coord):
    return abs(coord[0]) + abs(coord[1])

def findShortestManhattenDistance(coords):
    shortest = findManhattenDistance(coords[0])
    for coord in coords:
        nextDistance = findManhattenDistance(coord)
        if nextDistance < shortest:
            shortest = nextDistance
    return shortest

def findShortestRealDistance(path1, path2, coords):
    shortest = 999999999
    for coord in coords:
        path1Matches = [dist for ((c), dist) in path1 if c == coord]
        path2Matches = [dist for ((c), dist) in path2 if c == coord]
        thisDistance = min(path1Matches) + min(path2Matches)
        if thisDistance < shortest:
            shortest = thisDistance
    return shortest

path1 = tracePath(path1Instructions)
path2 = tracePath(path2Instructions)
intersections = findIntersections(path1, path2)
# Part 1
print(findShortestManhattenDistance(intersections))
# Part 2
print(findShortestRealDistance(path1, path2, intersections))
