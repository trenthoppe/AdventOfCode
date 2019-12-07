# Read input and get wire paths
file = open("input.txt", "r")
# splitlines() to remove newline characters
lines = file.read().splitlines()
wirePath1 = lines[0].split(',')
wirePath2 = lines[1].split(',')
print(wirePath1)
print(wirePath2)