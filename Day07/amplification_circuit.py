import itertools

# Read input and get codes
file = open("input.txt", "r")
program = list(map(int, file.readline().split(',')))

# Thermal Environment Supervision Terminal (TEST)
class TEST(object):
    def __init__(self, diagnosticProgram):
        # Shallow copy of diagnostic program
        self.program = diagnosticProgram[:]
        self.backup = diagnosticProgram[:]
        self.instructionIndex = 0
        self.outputs = []

    # Operations 
    class Operation:
        def __init__(self, opFunc, paramCount, isWriteOp, isJumpOp):
            self.execute = opFunc
            self.paramCount = paramCount
            self.isWriteOperation = isWriteOp
            self.isJumpOperation = isJumpOp
            
    def add(self, params):
        self.program[params[2]] = params[0] + params[1]

    def mult(self, params):
        self.program[params[2]] = params[0] * params[1]
    
    def readIn(self, params):
        self.program[params[0]] = params[1]

    def output(self, params):
        self.outputs.append(params[0])

    def jumpIfTrue(self, params):
        if params[0] != 0:
            self.instructionIndex = params[1]
        else:
            self.instructionIndex += 3
    
    def jumpIfFalse(self, params):
        if params[0] == 0:
            self.instructionIndex = params[1]
        else:
            self.instructionIndex += 3

    def lessThan(self, params):
        self.program[params[2]] = 1 if params[0] < params[1] else 0
    
    def equals(self, params):
        self.program[params[2]] = 1 if params[0] == params[1] else 0

    operationsDict = {
        1: Operation(add, 3, True, False),
        2: Operation(mult, 3, True, False),
        3: Operation(readIn, 1, True, False),
        4: Operation(output, 1, False, False),
        5: Operation(jumpIfTrue, 2, False, True),
        6: Operation(jumpIfFalse, 2, False, True),
        7: Operation(lessThan, 3, True, False),
        8: Operation(equals, 3, True, False),
    }

    # Reset the program to its initial state
    def resetProgram(self):
        self.instructionIndex = 0
        self.program = self.backup[:]

    # Take an instruction and deserialize it into (opCode, paramModes) e.g. 1002 -> (2, "010")
    def deserializeInstruction(self, instruction):
        # prepend instruction with 0's for missing param mode values
        instructionString = str(instruction)
        zerosNeeded = 5-len(instructionString)
        instructionString = ("0" * zerosNeeded) + instructionString
        # get the op code from last two characters in instruction
        opCode = int(instructionString[-2:])
        # the rest of the instruction are the param modes
        paramModes = instructionString[:-2] 
        return (opCode, paramModes)

    # Get the values for our operations based on the param mode
    def deserializeParamModes(self, instruction):
        opCode = instruction[0]
        paramModes = instruction[1]
        paramCount = self.operationsDict[opCode].paramCount
        isWriteOp = self.operationsDict[opCode].isWriteOperation
        values = []
        for i in range(1, paramCount+1):
            # read modes from right to left because the 'rightmost' param mode 
            # corresponds to the 'leftmost' param
            mode = paramModes[len(paramModes)-i]
            param = self.program[self.instructionIndex+i]
            # if it is write op, the destination cannot be immediate
            if i==paramCount and isWriteOp:
                value = param
            else:
                # otherwise check to see if it is in read or immediate mode and capture the value
                value = self.program[param] if mode == '0' else param
            values.append(value)
        return values
    
    def runProgram(self, input):
        nextInputIndex = 0
        output = None
        #print(input)
        # Iterate through ops until 99 hault
        while True:
            currentInstruction = self.deserializeInstruction(self.program[self.instructionIndex])

            # Look at the op and hault if 99
            opCode = currentInstruction[0]
            if opCode == 99:
                break
            
            # Retrieve the values for our operation
            operationValues = self.deserializeParamModes(currentInstruction)

            # If we run out of input when the program is expecting more,
            # hault and wait for more input
            if opCode == 3:
                if nextInputIndex < len(input):
                    operationValues.append(input[nextInputIndex])
                    nextInputIndex += 1
                else:
                    break
            elif opCode == 4:
                # Save output but finish running the program
                output = operationValues[0]

            # Lookup operation in our operation dictionary and execute
            operation = self.operationsDict[opCode]
            operation.execute(self, operationValues)
            
            # Update our instruction index unless we jumped
            if not operation.isJumpOperation:
                self.instructionIndex += operation.paramCount + 1
        
        return output

class Amplifier:
    def __init__(self, controlSoftware):
        self.controlSoftware = controlSoftware[:]
        self.test = TEST(self.controlSoftware)
    
    def setPhaseSetting(self, phaseSetting):
        self.test.runProgram([phaseSetting])

    def run(self, input):
        output = self.test.runProgram([input])
        return output

class AmplificationCircuit:
    def __init__(self, test, phaseSettingRange):
        self.TEST = test
        self.amplifiers = []
        self.allPhaseSettings = list(itertools.permutations(phaseSettingRange))
    
    def initializeAmplifiers(self, phaseSettings):
        self.amplifiers = []
        for phaseSetting in phaseSettings:
            amp = Amplifier(self.TEST.program)
            amp.setPhaseSetting(phaseSetting)
            self.amplifiers.append(amp)

    def runAmplificationCircuit(self):
        prevCircuitOutput = 0
        circuitComplete = False
        while not circuitComplete:
            for amplifier in self.amplifiers:
                output = amplifier.run(prevCircuitOutput)

                # If there is no output, our circuit has completed
                if output is None:
                    circuitComplete = True
                    break
                
                prevCircuitOutput = output
    
        return prevCircuitOutput
    
    def findMaxOutputSignal(self):
        maxOutputSignal = 0
        for phaseSettings in self.allPhaseSettings:
            self.initializeAmplifiers(phaseSettings)
            nextOutputSignal = self.runAmplificationCircuit()
            if nextOutputSignal > maxOutputSignal:
                maxOutputSignal = nextOutputSignal
        return maxOutputSignal


# Run execution
test = TEST(program)
print(AmplificationCircuit(test, range(5,10)).findMaxOutputSignal())
