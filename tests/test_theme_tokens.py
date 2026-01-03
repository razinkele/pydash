from pathlib import Path


def test_css_tokens_present():
    css_path = (
        Path(__file__).parent.parent
        / "src"
        / "bs4dash_py"
        / "assets"
        / "bs4dash_styles.css"
    )
    content = css_path.read_text(encoding="utf-8")

    # Assert new tokens are present
    assert "--bs4dash-badge-success-bg" in content
    assert "--bs4dash-nav-active-bg" in content
    assert "--bs4dash-border-radius" in content
    assert "--bs4dash-spacing-md" in content
    assert "--bs4dash-radius-sm" in content

    # Assert mapping rules exist
    assert ".nav-link.active" in content
    assert ".badge.badge-success" in content


def test_theme_renders_new_tokens():
    from bs4dash_py.theme import Theme

    t = Theme({"bs4dash-border-radius": "5px", "bs4dash-spacing-md": "0.75rem"})
    css = t.to_css()
    assert "--bs4dash-border-radius: 5px;" in css
    assert "--bs4dash-spacing-md: 0.75rem;" in css
