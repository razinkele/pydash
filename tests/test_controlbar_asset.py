import pytest


def test_dashboard_page_references_controlbar_asset():
    pytest.importorskip("shiny")
    from bs4dash_py import dashboard_page_shiny

    page = dashboard_page_shiny()
    html = str(page)
    # The page should reference the controlbar asset filename or the handler name
    assert "bs4dash_controlbar.js" in html or "bs4dash_controlbar" in html
