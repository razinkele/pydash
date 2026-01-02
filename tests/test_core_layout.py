def test_core_layout_shiny():
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

    # Ensure shiny helpers exist
    assert hasattr(mod, "body_shiny")
    assert hasattr(mod, "footer_shiny")

    # Basic rendering smoke checks
    from shiny import ui

    body = mod.body_shiny(
        ui.tags.div({"class": "row"}, ui.tags.div({"class": "col-12"}, "content"))
    )
    assert "content-wrapper" in str(body)

    footer = mod.footer_shiny(
        "My footer", left=ui.tags.span("L"), right=ui.tags.span("R")
    )
    assert "main-footer" in str(footer)
