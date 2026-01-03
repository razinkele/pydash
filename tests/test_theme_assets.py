from pathlib import Path

from bs4dash_py import (
    bootswatch_href,
    register_asset_provider,
    resolve_asset,
    unregister_asset_provider,
)


def test_default_bootswatch_prefers_vendored(tmp_path, monkeypatch):
    # Create a fake vendored theme
    base = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "bs4dash_py"
        / "assets"
        / "bootswatch"
    )
    tdir = base / "__test_theme__"
    tdir.mkdir(parents=True, exist_ok=True)
    css = tdir / "bootstrap.min.css"
    css.write_text("/* vendored bootstrap stub */", encoding="utf-8")

    try:
        href = bootswatch_href("__test_theme__")
        assert href.startswith("file:") or href.startswith("file://")
    finally:
        css.unlink()
        tdir.rmdir()


def test_register_custom_bootswatch_provider(monkeypatch):
    def custom(name, version="5"):
        if name == "plug":
            return "https://custom.example/plug.css"
        return None

    register_asset_provider("bootswatch", custom, prepend=True)
    try:
        assert resolve_asset("bootswatch", "plug") == "https://custom.example/plug.css"
        assert bootswatch_href("plug") == "https://custom.example/plug.css"
    finally:
        unregister_asset_provider("bootswatch", custom)
