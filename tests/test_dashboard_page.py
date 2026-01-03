def test_dashboard_page_includes_adminlte_assets():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import dashboard_page_shiny

    page = dashboard_page_shiny(
        adminlte_css="/css/adminlte.css", adminlte_js="/js/adminlte.js"
    )
    s = str(page)
    assert "/css/adminlte.css" in s
    assert "src=/js/adminlte.js" in s or "/js/adminlte.js" in s


def test_dashboard_page_inlines_fallback_assets_when_include_missing(monkeypatch):
    import pytest

    pytest.importorskip("shiny")
    # Simulate include_js and include_css not available or raising
    from shiny import ui

    from bs4dash_py import dashboard_page_shiny

    # Backup and remove/replace include_js/include_css
    orig_include_js = getattr(ui, "include_js", None)
    orig_include_css = getattr(ui, "include_css", None)

    monkeypatch.setattr(
        ui, "include_js", lambda *a, **k: (_ for _ in ()).throw(Exception("no"))
    )
    monkeypatch.setattr(
        ui, "include_css", lambda *a, **k: (_ for _ in ()).throw(Exception("no"))
    )

    page = dashboard_page_shiny()
    s = str(page)
    # Expect fallback inline handler or identifier present
    assert "bs4dash_controlbar" in s
    assert "user-avatar-initials" in s

    # restore
    if orig_include_js is not None:
        monkeypatch.setattr(ui, "include_js", orig_include_js)
    if orig_include_css is not None:
        monkeypatch.setattr(ui, "include_css", orig_include_css)
