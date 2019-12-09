def isValid(password):
    passwordSet = set(password)

    if len(passwordSet) == len(password):
        return False

    for i in range(1, len(password)):
        if int(password[i-1]) > int(password[i]):
            return False
    # Part 1
    # return True

    # Part 2
    digitCounts = []
    for digit in passwordSet:
        digitCounts.append(password.count(digit))

    return 2 in digitCounts

def countValid(start, end):
    validsCount = 0
    for i in range(start, end):
        if isValid(str(i)):
            validsCount += 1
    return validsCount

print(countValid(156218, 652527))