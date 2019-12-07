# Read input and get codes
file = open("input.txt", "r")
codes = list(map(int, file.readline().split(',')))

# Execute opcodes
def executeOpcodes(codes, noun, verb):
    # Shallow copy of codes
    _codes = codes[:]
    # Set initial noun/verb
    _codes[1] = noun
    _codes[2] = verb
    # Iterate through ops until 99 hault
    opIndex = 0
    currentOp = _codes[opIndex]
    while currentOp != 99:
        pos1 = _codes[opIndex+1]
        pos2 = _codes[opIndex+2]
        dest = _codes[opIndex+3]

        if currentOp == 1:
            opCalcResult = _codes[pos1] + _codes[pos2]
        elif currentOp == 2:
            opCalcResult = _codes[pos1] * _codes[pos2]
        else:
            print("Unknown op")
        
        _codes[dest] = opCalcResult
        opIndex += 4
        currentOp = _codes[opIndex]
    return _codes[0]

def findNounVerb(codes, target):
    # Run initial condition
    noun = 0
    verb = 0
    result = executeOpcodes(codes, noun, verb)

    while result != target:
        # Get next noun/verb combo
        if verb == 99:
            verb = 0
            noun += 1
        elif noun <= 99:
            verb += 1
        else:
            print("Couldn't find Noun/Verb")

        # Recopy initial codes, set noun/verb, and execute ops
        result = executeOpcodes(codes, noun, verb)
    
    return str(noun) + str(verb)

# Run execution
# Part 1
print(executeOpcodes(codes, 12, 2))
# Part 2
print(findNounVerb(codes, 19690720))