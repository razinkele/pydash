def test_shiny_imports():
    import importlib
    import os
    import sys

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(repo_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    mod = importlib.import_module("bs4dash_py")
    # Ensure the shiny wrapper functions exist (they are lazy and won't import shiny until used)
    assert hasattr(mod, "dashboard_page_shiny")
    assert hasattr(mod, "navbar_shiny")
    assert hasattr(mod, "sidebar_shiny")
    assert hasattr(mod, "box_shiny")
