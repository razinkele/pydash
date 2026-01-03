def test_theme_to_css_and_style_tag():
    from bs4dash_py.theme import Theme, theme_tag

    t = Theme({"bs4dash-avatar-bg": "#112233", "primary": "#0b5e2e"})
    css = t.to_css()
    assert "--bs4dash-avatar-bg: #112233;" in css
    assert "--primary: #0b5e2e;" in css

    st = theme_tag(t)
    # When running in test env without shiny, theme_tag returns raw css string
    assert isinstance(st, str) and "--bs4dash-avatar-bg" in st