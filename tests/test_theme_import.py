def test_theme_importable():
    """Ensure Theme can be imported from the package root and behaves as expected."""
    from bs4dash_py import Theme

    t = Theme.from_bslib({"bg": "#ffffff", "primary": "#00f"})
    css = t.to_css()
    assert "--bs4dash-nav-bg" in css
    assert "--bs4dash-primary-bg" in css
