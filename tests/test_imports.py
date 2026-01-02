import os
import sys


def test_imports():
    # Make local src visible for tests when the package isn't installed
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(repo_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    import importlib

    mod = importlib.import_module("bs4dash_py")
    assert hasattr(mod, "dashboard_page")
    assert hasattr(mod, "navbar")
    assert hasattr(mod, "sidebar")
    assert hasattr(mod, "box")
