import importlib
import os
import sys

sys.path.insert(0, os.path.abspath("src"))
try:
    importlib.import_module("bs4dash_py.shiny_layout")
    print("imported OK")
except Exception:
    import traceback

    traceback.print_exc()
    raise
