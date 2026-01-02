# bs4dash-py (MVP)

[![CI](https://github.com/razinkele/pydash/actions/workflows/ci.yml/badge.svg)](https://github.com/razinkele/pydash/actions/workflows/ci.yml) [Distributions (Artifacts)](https://github.com/razinkele/pydash/actions?query=workflow%3ACI) [![PyPI](https://img.shields.io/pypi/v/bs4dash-py.svg)](https://pypi.org/project/bs4dash-py/)

> Note: The PyPI badge will show the latest published version once `bs4dash-py` has been released to PyPI.

Minimal MVP to provide AdminLTE3/Bootstrap4-style dashboard building blocks for Shiny for Python.

Quick start

1. Install: `pip install -e .` (in project root)
2. Run example: `python examples/mvp_shiny.py`

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
