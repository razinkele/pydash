def test_theme_to_css_and_style_tag():
    from bs4dash_py.theme import Theme, theme_tag

    t = Theme({"bs4dash-avatar-bg": "#112233", "primary": "#0b5e2e"})
    css = t.to_css()
    assert "--bs4dash-avatar-bg: #112233;" in css
    assert "--primary: #0b5e2e;" in css

    st = theme_tag(t)
    # Accept either raw CSS string (no Shiny available) or a style tag; check rendered content.
    rendered = st if isinstance(st, str) else str(st)
    assert "--bs4dash-avatar-bg" in rendered


def test_to_style_tag_with_id(monkeypatch):
    from bs4dash_py.theme import Theme

    # Simulate shiny.ui tags when available
    class FakeUI:
        class tags:
            @staticmethod
            def style(css, **attrs):
                aid = attrs.get("id")
                return f'<style id="{aid}">{css}</style>'

    import bs4dash_py.theme as theme_mod

    monkeypatch.setattr(theme_mod, "ui", FakeUI())

    t = Theme({"bs4dash-avatar-bg": "#112233"})
    rendered = t.to_style_tag(id="theme-styles")
    assert 'id="theme-styles"' in rendered
    assert "--bs4dash-avatar-bg" in rendered


def test_theme_from_bootswatch_helpers(monkeypatch):
    from bs4dash_py.theme import Theme

    # Create a Theme from bootswatch
    t = Theme.from_bootswatch("flatly")
    href = t.bootswatch_href()
    assert href is not None

    # Simulate bootswatch_tag using fake shiny UI
    class FakeUI:
        class tags:
            @staticmethod
            def link(attrs):
                return f"<link rel=\"stylesheet\" href=\"{attrs['href']}\" />"

            @staticmethod
            def style(css, **attrs):
                aid = attrs.get("id")
                return f'<style id="{aid}">{css}</style>'

    import bs4dash_py.theme as theme_mod

    monkeypatch.setattr(theme_mod, "ui", FakeUI())

    tag = t.bootswatch_tag(as_tag=True)
    rendered = tag if isinstance(tag, str) else str(tag)
    assert "flatly" in rendered

    # Verify to_head_elements returns both parts
    link, style = t.to_head_elements(id="theme-styles", link_as_tag=True)
    assert link is not None and "flatly" in (
        link if isinstance(link, str) else str(link)
    )
    assert style is not None and 'id="theme-styles"' in (
        style if isinstance(style, str) else str(style)
    )


def test_theme_to_head_elements_without_bootswatch(monkeypatch):
    from bs4dash_py.theme import Theme

    class FakeUI:
        class tags:
            @staticmethod
            def style(css, **attrs):
                aid = attrs.get("id")
                return f'<style id="{aid}">{css}</style>'

    import bs4dash_py.theme as theme_mod

    monkeypatch.setattr(theme_mod, "ui", FakeUI())

    t = Theme({"bs4dash-avatar-bg": "#112233"})
    link, style = t.to_head_elements(id="theme-styles")
    assert link is None
    assert style is not None and 'id="theme-styles"' in style


def test_from_bslib_conversion():
    from bs4dash_py.theme import Theme

    bslib_data = {
        "bg": "#111111",
        "fg": "#222222",
        "primary": "#ff00ff",
        "info": "#00ffff",
        "base_font": "Inter, sans-serif",
        "bootswatch": "flatly",
    }

    t = Theme.from_bslib(bslib_data)
    css = t.to_css()
    # Check that mapped tokens appear in the generated CSS
    assert "--bs4dash-nav-bg: #111111;" in css
    assert "--bs4dash-nav-fg: #222222;" in css
    assert "--bs4dash-primary-bg: #ff00ff;" in css
    assert "--bs4dash-badge-info-bg: #00ffff;" in css
    assert "--bs4dash-base-font: Inter, sans-serif;" in css
    # bootswatch should be registered on the Theme instance
    assert t._bootswatch_name == "flatly"
