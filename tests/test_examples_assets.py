import importlib


def _reload_example_with_env(monkeypatch, env):
    # Set env vars and reload the small bootswatch helper module so
    # module-level values are recalculated without importing the full example
    for k, v in env.items():
        if v is None:
            monkeypatch.delenv(k, raising=False)
        else:
            monkeypatch.setenv(k, v)
    import examples._bootswatch as bw

    return importlib.reload(bw)


def test_get_bootswatch_href_respects_env(monkeypatch):
    mod = _reload_example_with_env(monkeypatch, {"PYBS4DASH_BOOTSWATCH_SRC": "cdn"})
    href = mod.get_bootswatch_href("flatly")
    assert "cdn.jsdelivr.net" in href

    mod = _reload_example_with_env(monkeypatch, {"PYBS4DASH_BOOTSWATCH_SRC": "local"})
    href_local = mod.get_bootswatch_href("flatly")
    # Should equal bootswatch_href from the package (which prefers vendored copy when present)
    from bs4dash_py import bootswatch_href

    assert href_local == bootswatch_href("flatly")


def test_list_vendored_bootswatch_has_valid_shape():
    from bs4dash_py import list_vendored_bootswatch

    themes = list_vendored_bootswatch()
    assert isinstance(themes, list)
    # If no vendored themes, that's OK (we can't force vendoring here); just check type
    # If vendored themes exist, ensure they have expected files on disk
    if themes:
        from pathlib import Path

        for t in themes:
            p = (
                Path(__file__).resolve().parents[1]
                / "src"
                / "bs4dash_py"
                / "assets"
                / "bootswatch"
                / t
                / "bootstrap.min.css"
            )
            assert p.exists(), f"Vendored theme file missing for {t}: {p}"
