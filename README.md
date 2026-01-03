# bs4dash-py (MVP)

[![CI](https://github.com/razinkele/pydash/actions/workflows/ci.yml/badge.svg)](https://github.com/razinkele/pydash/actions/workflows/ci.yml) [Distributions (Artifacts)](https://github.com/razinkele/pydash/actions?query=workflow%3ACI) [![PyPI](https://img.shields.io/pypi/v/bs4dash-py.svg)](https://pypi.org/project/bs4dash-py/)

> Note: The PyPI badge will show the latest published version once `bs4dash-py` has been released to PyPI.

Minimal MVP to provide AdminLTE3/Bootstrap4-style dashboard building blocks for Shiny for Python.

Quick start

1. Install: `pip install -e .` (in project root)
2. Run example: `python examples/mvp_shiny.py` or `python examples/mvp_shiny_from_bslib.py`

Examples

- Run the Shiny example that demonstrates converting a bslib-like theme to a `bs4dash` Theme:

```bash
python -m pip install -e '.[dev]'
pip install shiny
# Run the example (default port 8000)
python examples/mvp_shiny_from_bslib.py
```

Environment variables supported by the example:

- `PYBS4DASH_PORT` — Port to run the example on (default: 8000).
- `PYBS4DASH_ADMINLTE` / `PYBS4DASH_ADMINLTE_JS` — Provide local paths (instead of CDN URLs) to inline AdminLTE CSS or JS for deterministic CI tests.
- `PYBS4DASH_BOOTSWATCH_SRC` — `local` (default) or `cdn`. When set to `cdn`, the Bootswatch theme CSS will be loaded from jsdelivr; when `local` the example will prefer vendored files when present.
- `PYBS4DASH_BOOTSWATCH_THEME` — Bootswatch theme name to use when applying Bootswatch from the example (default: `flatly`).

Vendor script

- Use `scripts/vendor_assets.py` to vendor AdminLTE and Bootswatch themes into `src/bs4dash_py/assets` so tests and CI can use deterministic local assets without relying on CDNs.

Examples:

```bash
# Vendor AdminLTE from CDN into src assets
python scripts/vendor_assets.py --adminlte "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css" --adminlte-js "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

# Vendor Bootswatch themes
python scripts/vendor_assets.py --bootswatch flatly,cyborg

# Vendor from local sources
python scripts/vendor_assets.py --adminlte-local tests/assets/adminlte.min.css --bootswatch-local flatly=tests/stubs/bootswatch_stub.min.css
```
Git LFS (recommended for large assets)

- Large binary assets (e.g., `adminlte.min.css`) are better managed with Git LFS to avoid bloating the repository history.
- To opt in locally:
  1. Install Git LFS: `git lfs install`.
  2. Track files: `git lfs track "src/bs4dash_py/assets/*.min.css"` (this will create/update `.gitattributes`).
  3. If you need to convert the existing committed file to LFS (rewrites history): `git lfs migrate import --include="src/bs4dash_py/assets/adminlte.min.css"` (use with caution; coordinate with maintainers).
Tip: In CI set `PYBS4DASH_BOOTSWATCH_SRC=local` and provide local `ADMINLTE` assets to avoid external network dependencies and flaky CDN DNS/blocked requests.

Documentation

- Layout helpers (sidebar, navbar, breadcrumbs): `docs/layout_index.md`
- Theming: `docs/themes.md` (CSS variables and tokens you can override in your app)
- Server helper behavior (sync & async): `docs/server_helpers.md`
- Examples gallery and screenshots: `docs/gallery.md`

Note: The gallery job can optionally push generated images to a branch using a Personal Access Token stored in the `GALLERY_PUSH_TOKEN` repository secret. See `docs/gallery.md` → "Publishing generated images automatically (optional)" for setup instructions.

Build artifacts

- The CI packaging job uploads built distributions as workflow artifacts (name: `distributions-<run_id>`).
- To download the latest wheel/sdist:
  1. Visit the CI workflow page: https://github.com/razinkele/pydash/actions/workflows/ci.yml
  2. Open the latest successful run and click **Artifacts** → download the `distributions-<run_id>` zip and extract the wheel/sdist.

Server helpers (sync & async)

- Server helpers such as `update_sidebar`, `update_navbar_tabs`, and `show_controlbar` will accept both synchronous session APIs and asynchronous session APIs (i.e., `async def` methods or methods that return awaitables). See the full documentation: `docs/server_helpers.md`.
- The helpers detect awaitables and will: run to completion if no running loop is found, schedule on the current loop with `create_task` if present, or use `asyncio.run_coroutine_threadsafe` when the loop runs in another thread. This avoids un-awaited coroutine warnings and supports a variety of Shiny session implementations.

Example:

```py
from bs4dash_py import update_sidebar

# works with sync session
update_sidebar(session, [{"text": "Home", "href": "#"}])

# also works when session.send_custom_message is async
# (helper will await/schedule the coroutine)
update_sidebar(session, [{"text": "Updates", "href": "#updates"}])
```

Contributing

- See `CONTRIBUTING.md` for development setup, running tests and hooks.

Draft PR: scaffold and CI added
