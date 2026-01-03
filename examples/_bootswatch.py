import os

from bs4dash_py import bootswatch_href

BOOTSWATCH_SRC = os.environ.get("PYBS4DASH_BOOTSWATCH_SRC", "local").lower()
BOOTSWATCH_DEFAULT_THEME = os.environ.get("PYBS4DASH_BOOTSWATCH_THEME", "flatly")


def get_bootswatch_href(name: str, version: str = "5") -> str:
    """Return the Bootswatch href based on environment preference.

    - If `PYBS4DASH_BOOTSWATCH_SRC=cdn` returns a CDN URL (jsdelivr)
    - Otherwise returns the library helper `bootswatch_href(name)` which
      prefers a vendored file when present for deterministic tests.
    """
    if BOOTSWATCH_SRC == "cdn":
        return f"https://cdn.jsdelivr.net/npm/bootswatch@{version}/dist/{name}/bootstrap.min.css"
    return bootswatch_href(name, version=version)
