import sys
import traceback

import yaml

path = sys.argv[1]
try:
    with open(path, "r", encoding="utf-8") as f:
        yaml.safe_load(f)
    print("OK")
except Exception:
    traceback.print_exc()
    print("---repr of lines 40-48---")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, start=1):
        if 40 <= i <= 48:
            print(i, repr(line))
