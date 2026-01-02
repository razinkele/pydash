def test_shiny_layout_import():
    import importlib
    import os
    import sys

    import pytest

    # Skip this test if Shiny is not installed in the environment
    pytest.importorskip("shiny")

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(repo_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    importlib.import_module("bs4dash_py.shiny_layout")
