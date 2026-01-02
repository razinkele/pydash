def test_styles_define_tokens():
    from pathlib import Path
    p = Path(__file__).parents[1] / "src" / "bs4dash_py" / "assets" / "bs4dash_styles.css"
    txt = p.read_text()
    assert "--bs4dash-avatar-bg" in txt
    assert "--bs4dash-avatar-fg" in txt
