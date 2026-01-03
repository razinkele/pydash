"""Download a local copy of axe-core into `tests/assets/axe.min.js`.

This script will try a few public CDNs and pick the first that succeeds.
Run this script manually (e.g., in your `shiny` env) to vendor the file for CI.
"""

import urllib.request
from pathlib import Path

URLS = [
    "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.3/axe.min.js",
    "https://cdn.jsdelivr.net/npm/axe-core@4.9.3/axe.min.js",
    "https://unpkg.com/axe-core@4.9.3/axe.min.js",
    # try generic latest package endpoints
    "https://cdn.jsdelivr.net/npm/axe-core/axe.min.js",
    "https://unpkg.com/axe-core/axe.min.js",
]
OUT = Path(__file__).resolve().parent.parent / "tests" / "assets" / "axe.min.js"
OUT.parent.mkdir(parents=True, exist_ok=True)

for url in URLS:
    print(f"Trying {url}...")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
            if len(data) < 100:
                print(
                    f"Fetched {len(data)} bytes from {url}, looks too small, trying next"
                )
                continue
            OUT.write_bytes(data)
            print(f"Downloaded {url} -> {OUT}")
            break
    except Exception as e:
        print(f"Failed to download from {url}: {e}")
else:
    raise SystemExit(
        "Could not download axe.min.js from known CDNs; please vendor it manually into tests/assets/"
    )
