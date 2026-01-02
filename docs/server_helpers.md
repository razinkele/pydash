# Server helpers — sync & async behavior 🔧

This document explains how the package's server-side helpers (for example:
`update_sidebar`, `update_navbar_tabs`, `show_controlbar`) handle **both
synchronous and asynchronous** session APIs.

Why this matters
- Different Shiny server/session implementations expose different APIs:
  some provide synchronous `send_*` methods, others expose `async def`
  coroutine methods or methods that return awaitables.
- If a coroutine is produced but never awaited, Python emits a
  "coroutine was never awaited" RuntimeWarning — which we avoid here.

Behavior details
- Detection:
  - Helpers attempt to call several candidate session methods (e.g.
    `send_custom_message`, `send_message`, `send`, `sendInputMessage`).
  - If the session method is an async function or returns an awaitable,
    the helper detects that and handles it safely.

- Scheduling strategy (best-effort):
  1. If there is no running event loop on the current thread, the
     coroutine is executed to completion using `asyncio.run`.
  2. If there is a running loop on the current thread, the coroutine is
     scheduled on that loop with `loop.create_task`.
  3. If the loop is running in a different thread, the coroutine is
     scheduled in a thread-safe fashion using
     `asyncio.run_coroutine_threadsafe` (preferred for cross-thread loops).
  4. As a final fallback, the helper attempts `asyncio.ensure_future`.

These strategies are applied to both:
- async session methods (i.e., `async def send_custom_message(...)`) and
- synchronous methods that return awaitables.

Notes & caveats
- The helper uses a best-effort approach and intentionally swallows
  transient scheduling errors so that user apps are not interrupted by
  message delivery issues.
- Tests exist that exercise same-thread scheduling, cross-thread
  scheduling (background loop), and no-loop behavior.

Example
```py
from bs4dash_py import update_sidebar

# Works for sync session APIs
update_sidebar(session, [{"text": "Home", "href": "#"}])

# Works for async session APIs too
# (e.g., when session.send_custom_message is `async def`)
update_sidebar(session, [{"text": "Updates", "href": "#updates"}])
```

Further reading
- Tests: `tests/test_server_updates.py` — shows how we validate these
  behaviors (including real background event loop scheduling).
