import sys

path = sys.argv[1]
lineno = int(sys.argv[2])
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(repr(lines[lineno - 1]))
