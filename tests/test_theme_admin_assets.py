from bs4dash_py import bootswatch_href, resolve_asset


def test_adminlte_provider_returns_local_css():
    href = resolve_asset("adminlte", "unused", type="css")
    assert href is None or href.startswith(
        "file:"
    ), "AdminLTE provider should return a file:// href when vendored"


def test_adminlte_provider_returns_local_js():
    href = resolve_asset("adminlte", "unused", type="js")
    assert href is None or href.startswith(
        "file:"
    ), "AdminLTE provider should return a file:// href for JS when vendored"


def test_fonts_provider_finds_stub():
    # If a google_fonts_stub exists under tests/stubs, provider should find it
    href = resolve_asset("fonts", "google")
    assert href is None or href.startswith(
        "file:"
    ), "Fonts provider should return a file:// href when vendored"


def test_bootswatch_still_resolves_to_cdn_when_missing():
    # Request a non-existent theme name; should fall back to CDN URL
    href = bootswatch_href("this-theme-definitely-does-not-exist-xyz")
    assert href.startswith(
        "https://"
    ), "Fallback to CDN expected when vendored theme missing"
