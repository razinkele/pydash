def test_brand_and_controlbar():
    import importlib
    import os
    import sys
    import pytest

    pytest.importorskip("shiny")

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(repo_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    mod = importlib.import_module("bs4dash_py")
    assert hasattr(mod, "dashboard_brand_shiny")
    assert hasattr(mod, "controlbar_shiny")

    from shiny import ui

    brand = mod.dashboard_brand_shiny("Acme", color="primary", href="/home")
    assert "brand-link" in str(brand)
    assert "Acme" in str(brand)

    cb = mod.controlbar_shiny(ui.tags.p("x"), dark=False)
    assert "control-sidebar" in str(cb)
    assert "control-sidebar-light" in str(cb)
