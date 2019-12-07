opArr = []
i = 0
with open("input.rtf", "r") as filestream:
    for line in filestream:
            opArr = int(line.split(","))
            i += 1

print(opArr)