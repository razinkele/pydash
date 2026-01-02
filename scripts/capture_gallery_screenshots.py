"""Capture screenshots of example Shiny apps for the docs gallery.

Usage:
    python scripts/capture_gallery_screenshots.py --examples examples/mvp_shiny.py --out docs/images --port 9000

Prerequisites:
- Playwright Python package and browsers installed: `pip install playwright` and `playwright install`
- A Shiny-capable Python environment and any runtime deps for the example apps

This script:
- launches each example in a subprocess with a free port (or provided port)
- waits for the server to respond
- uses Playwright to open the page and capture a screenshot of the main wrapper element
- saves screenshots into the output folder (default: `docs/images`)

The images can then be embedded in `docs/gallery.md`.
"""

import argparse
import os
import subprocess
import socket
import sys
import time
from pathlib import Path


def find_free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def wait_for_server(port, timeout=20.0):
    import urllib.request

    deadline = time.time() + timeout
    last_err = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
                _ = resp.read()
                return True
        except Exception as e:
            last_err = e
            time.sleep(0.2)
    raise RuntimeError(f"Server did not respond in time: {last_err}")


def create_thumbnail(image_path: Path, thumb_dir: Path, max_width: int = 600):
    """Create a thumbnail for `image_path` in `thumb_dir` with width `max_width`.

    Uses Pillow (PIL). Raises an informative ImportError if Pillow is missing.
    """
    try:
        from PIL import Image
    except Exception as e:
        raise ImportError("Pillow is required to create thumbnails. Install with 'pip install Pillow'.") from e

    thumb_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path) as im:
        w, h = im.size
        if w <= max_width:
            # copy instead of resizing
            out = thumb_dir / f"{image_path.stem}_thumb.png"
            im.save(out)
            return out
        new_h = int(max_width * h / w)
        im = im.resize((max_width, new_h), Image.LANCZOS)
        out = thumb_dir / f"{image_path.stem}_thumb.png"
        im.save(out)
        return out


def capture_one(example_path: Path, out_dir: Path, port: int):
    env = os.environ.copy()
    env["PYBS4DASH_PORT"] = str(port)

    proc = subprocess.Popen(
        [sys.executable, str(example_path)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    try:
        wait_for_server(port, timeout=20.0)

        try:
            from playwright.sync_api import sync_playwright
        except Exception as e:
            proc.terminate()
            raise RuntimeError("Playwright is required to capture screenshots. Install with 'pip install playwright' and run 'playwright install'.") from e

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}/", timeout=15000)

            # Try to screenshot the main wrapper; fallback to full page
            try:
                el = page.query_selector(".wrapper")
                img_path = out_dir / f"{example_path.stem}.png"
                if el:
                    el.screenshot(path=str(img_path))
                else:
                    page.screenshot(path=str(img_path), full_page=True)

                # Attempt to generate a thumbnail (optional; requires Pillow)
                try:
                    # create a 600px wide thumbnail by default
                    create_thumbnail(img_path, out_dir / "thumbs", max_width=600)
                except Exception:
                    # Pillow not available or thumbnail failed - skip silently
                    pass
            finally:
                browser.close()

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--examples", nargs="+", required=True, help="Example scripts to capture")
    p.add_argument("--out", default="docs/images", help="Output directory for screenshots")
    p.add_argument("--port", type=int, help="Optional fixed port to use (otherwise uses a free port per example)")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for ex in args.examples:
        ex_path = Path(ex)
        if not ex_path.exists():
            print(f"Skipping missing example: {ex}")
            continue
        port = args.port or find_free_port()
        print(f"Capturing {ex} on port {port} -> {out_dir / (ex_path.stem + '.png')}")
        try:
            capture_one(ex_path, out_dir, port)
        except Exception as e:
            print(f"Failed to capture {ex}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
