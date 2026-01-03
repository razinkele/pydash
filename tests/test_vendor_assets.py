import subprocess
import sys
from pathlib import Path

from scripts.vendor_assets import vendor_adminlte


def test_vendor_adminlte_from_local(tmp_path):
    # Use the tests/assets adminlte stub as a local source
    src = Path(__file__).resolve().parents[1] / "tests" / "assets" / "adminlte.min.css"
    assert src.exists(), "test asset missing"
    # vendor into tmp dir by calling internal function but adjust ASSETS_BASE via monkeypatch
    # Instead, copy to a temp dest by calling the function and checking return paths are writable
    res = vendor_adminlte(css_src=src.resolve().as_uri())
    assert isinstance(res, list)
    # cleanup
    for p in res:
        try:
            p.unlink()
        except Exception:
            pass


def test_vendor_bootswatch_local(tmp_path):
    # Simulate vendoring by creating a small file and using the local mapping logic
    fake_css = tmp_path / "fake_bootstrap.css"
    fake_css.write_text("/* fake */", encoding="utf-8")
    # Use subprocess to invoke CLI mapping and copy into src assets
    rv = subprocess.call(
        [
            sys.executable,
            "scripts/vendor_assets.py",
            "--bootswatch-local",
            f"__cli_test__={str(fake_css)}",
        ]
    )
    assert rv == 0
    # validate file exists in package assets
    dest = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "bs4dash_py"
        / "assets"
        / "bootswatch"
        / "__cli_test__"
        / "bootstrap.min.css"
    )
    assert dest.exists()
    # cleanup
    dest.unlink()
    dest.parent.rmdir()
