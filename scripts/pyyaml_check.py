import sys

import yaml

paths = sys.argv[1:]
for p in paths:
    print("---", p)
    try:
        with open(p, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        print("OK")
    except Exception as e:
        print("ERROR", e)
