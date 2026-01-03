def test_bootswatch_href_and_tag():
    from bs4dash_py.theme import bootswatch_href, bootswatch_tag

    href = bootswatch_href("flatly")
    # Accept either the CDN URL or a vendored local file URI
    assert (
        ("bootswatch" in href and "flatly" in href)
        or href.startswith("file:")
        or "assets/bootswatch" in href
    )

    tag = bootswatch_tag("flatly")
    # Accept either an href string or a link tag; verify it contains a reference to flatly
    rendered = tag if isinstance(tag, str) else str(tag)
    assert "flatly" in rendered


def test_bootswatch_invalid_name():
    import pytest

    from bs4dash_py.theme import bootswatch_href

    with pytest.raises(ValueError):
        bootswatch_href("")


def test_bootswatch_top_level_export_and_as_tag():
    import bs4dash_py

    # bootswatch_href should be available at the package root
    href = bs4dash_py.bootswatch_href("flatly")
    assert ("bootswatch" in href and "flatly" in href) or href.startswith("file:")

    # When as_tag=True we should get a link element (as a string or a tag-like object)
    from bs4dash_py.theme import bootswatch_tag

    tag = bootswatch_tag("flatly", as_tag=True)
    rendered = tag if isinstance(tag, str) else str(tag)
    assert rendered.strip().startswith("<link") and "flatly" in rendered


def test_vendored_bootswatch_file_exists():
    # Ensure the vendored files we rely on for deterministic CI exist
    from pathlib import Path

    base = Path(__file__).parent.parent / "src" / "bs4dash_py" / "assets" / "bootswatch"
    names = ["flatly", "cerulean", "solar"]
    for name in names:
        p = base / name / "bootstrap.min.css"
        assert p.exists(), f"Vendored {name} file missing: {p}"


def test_vendored_bootswatch_href_uses_local():
    # bootswatch_href should return a local file:// URI when vendored copy exists
    from bs4dash_py.theme import bootswatch_href

    for name in ["flatly", "cerulean", "solar"]:
        href = bootswatch_href(name)
        assert (
            href.startswith("file:") or "assets/bootswatch" in href
        ), f"Expected local href for {name}, got {href}"


def test_list_vendored_bootswatch():
    import bs4dash_py

    themes = bs4dash_py.list_vendored_bootswatch()
    assert isinstance(themes, list)
    assert "flatly" in themes
    assert "cerulean" in themes
    assert "solar" in themes


def test_serve_vendored_bootswatch_copies(tmp_path):
    from pathlib import Path

    import bs4dash_py

    dest = tmp_path / "static"
    copied = bs4dash_py.serve_vendored_bootswatch(dest)
    assert isinstance(copied, list)
    # Ensure files were actually copied
    for p in copied:
        assert Path(p).exists()
    # Ensure all vendored themes are available in dest
    themes = bs4dash_py.list_vendored_bootswatch()
    for t in themes:
        p = dest / t / "bootstrap.min.css"
        assert p.exists(), f"Expected {p} to exist"
