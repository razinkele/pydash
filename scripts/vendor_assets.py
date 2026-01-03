"""Vendor utility to fetch AdminLTE/Bootswatch assets into the package's
`src/bs4dash_py/assets` tree so CI and examples can use deterministic local
copies instead of relying on external CDNs.

Usage (examples):
  # vendor AdminLTE from a URL
  python scripts/vendor_assets.py --adminlte https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css

  # vendor Bootswatch themes (comma-separated list) using CDN
  python scripts/vendor_assets.py --bootswatch flatly,cyborg

  # OR use local file sources for testing
  python scripts/vendor_assets.py --adminlte-local tests/assets/adminlte.min.css --bootswatch-local flatly=tests/stubs/bootswatch_flatly.css

The script is intentionally small and depends only on the Python stdlib to
make it easy to run in CI.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]
ASSETS_BASE = ROOT / "src" / "bs4dash_py" / "assets"
BOOTSWATCH_DIR = ASSETS_BASE / "bootswatch"
ADMINLTE_CSS = ASSETS_BASE / "adminlte.min.css"
ADMINLTE_JS = ASSETS_BASE / "adminlte.min.js"


def _download_url_to(dest: Path, url: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # file:// URIs may contain percent-encoded characters; handle using
    # urllib utilities to convert to a local path reliably across platforms
    from urllib.parse import urlsplit
    from urllib.request import url2pathname

    parts = urlsplit(url)
    if parts.scheme == "file":
        src_path = Path(url2pathname(parts.path))
        if not src_path.exists():
            raise FileNotFoundError(f"Source file not found: {src_path}")
        shutil.copy2(src_path, dest)
        return
    # fallback to urllib for http/https
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    with open(dest, "wb") as fh:
        fh.write(data)


def vendor_adminlte(
    css_src: Optional[str] = None, js_src: Optional[str] = None
) -> list[Path]:
    """Vendor AdminLTE CSS and JS into `src/.../assets`.

    If `css_src`/`js_src` are None, do nothing (no-op). Sources may be URLs
    or local file paths.
    Returns list of files written.
    """
    written = []
    if css_src:
        css_src_url = (
            css_src
            if css_src.startswith("http") or css_src.startswith("file://")
            else Path(css_src).resolve().as_uri()
        )
        _download_url_to(ADMINLTE_CSS, css_src_url)
        written.append(ADMINLTE_CSS)
    if js_src:
        js_src_url = (
            js_src
            if js_src.startswith("http") or js_src.startswith("file://")
            else Path(js_src).resolve().as_uri()
        )
        _download_url_to(ADMINLTE_JS, js_src_url)
        written.append(ADMINLTE_JS)
    return written


def vendor_bootswatch(names: Iterable[str], version: str = "5") -> list[Path]:
    """Vendor a list of Bootswatch themes into `src/.../assets/bootswatch/<name>/bootstrap.min.css`.

    Names may be theme names (e.g., 'flatly'). Themes are fetched from the
    jsdelivr CDN. Returns list of written files.
    """
    written = []
    for name in names:
        out_dir = BOOTSWATCH_DIR / name
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / "bootstrap.min.css"
        url = f"https://cdn.jsdelivr.net/npm/bootswatch@{version}/dist/{name}/bootstrap.min.css"
        _download_url_to(dest, url)
        written.append(dest)
    return written


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--adminlte", help="URL to AdminLTE CSS file to vendor")
    p.add_argument("--adminlte-js", help="URL to AdminLTE JS file to vendor")
    p.add_argument(
        "--adminlte-local", help="Local path to AdminLTE CSS file (file path, copied)"
    )
    p.add_argument(
        "--bootswatch", help="Comma-separated Bootswatch theme names to vendor (cdn)"
    )
    p.add_argument(
        "--bootswatch-local",
        help="Comma-separated local mappings name=path to copy (e.g., flatly=./flatly.css)",
    )
    p.add_argument(
        "--version",
        default="5",
        help="Bootswatch version to use when fetching from CDN",
    )
    args = p.parse_args(argv)

    try:
        if args.adminlte or args.adminlte_local:
            css_src = args.adminlte_local or args.adminlte
            js_src = args.adminlte_js
            print(f"Vendoring AdminLTE from {css_src} {js_src}")
            written = vendor_adminlte(
                css_src
                and (
                    css_src
                    if css_src.startswith("file://") or css_src.startswith("http")
                    else Path(css_src).resolve().as_uri()
                ),
                js_src
                and (
                    js_src
                    if js_src.startswith("file://") or js_src.startswith("http")
                    else Path(js_src).resolve().as_uri()
                ),
            )
            for w in written:
                print("wrote", w)

        if args.bootswatch:
            names = [n.strip() for n in args.bootswatch.split(",") if n.strip()]
            print("Vendoring Bootswatch themes:", names)
            written = vendor_bootswatch(names, version=args.version)
            for w in written:
                print("wrote", w)

        if args.bootswatch_local:
            # parse mappings name=path, comma-separated
            items = [s.strip() for s in args.bootswatch_local.split(",") if s.strip()]
            for item in items:
                if "=" not in item:
                    print("Invalid mapping, expected name=path:", item, file=sys.stderr)
                    return 2
                name, path = item.split("=", 1)
                dest_dir = BOOTSWATCH_DIR / name
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / "bootstrap.min.css"
                src_path = Path(path)
                if not src_path.exists():
                    print("Source file not found:", src_path, file=sys.stderr)
                    return 2
                shutil.copy2(src_path, dest)
                print("wrote", dest)

        return 0
    except Exception as e:
        print("error:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
