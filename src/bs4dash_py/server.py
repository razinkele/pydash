import asyncio
import inspect
from typing import Any

"""Server-side helpers for sending custom messages to client-side handlers.

These helpers (e.g., `update_sidebar`, `update_navbar_tabs`, `show_controlbar`)
send custom messages to client JavaScript handlers. They are tolerant of
both synchronous session APIs (methods that perform sends immediately) and
asynchronous session APIs (async methods or methods that return awaitables).

Behavior when an async method or awaitable is detected:
- If no running event loop is found, the coroutine is run to completion via
  `asyncio.run`.
- If a running loop exists on the current thread, the coroutine is scheduled
  with `loop.create_task`.
- If a running loop exists on another thread, the coroutine is scheduled
  safely with `asyncio.run_coroutine_threadsafe`.

This reduces "coroutine was never awaited" warnings and works across a
variety of Shiny session implementations.
"""


def _send_controlbar_message(session: Any, action: str = "toggle") -> bool:
    """Send a controlbar message to the client using the Shiny session.

    Delegates to the generic `_send_custom_message` so both sync and async
    session APIs are handled consistently.
    """
    action = action or "toggle"
    payload = {"action": action}
    return _send_custom_message(session, "bs4dash_controlbar", payload)


# Generic custom message sender used by other helpers
def _send_custom_message(session: Any, name: str, payload: dict) -> bool:
    """Send a custom message to the client. Tries multiple session APIs.

    This function supports both synchronous and coroutine-based session
    methods. If the underlying method returns an awaitable or is an
    `async def`, it will be awaited when possible or scheduled as a task
    on the running loop.
    """
    candidates = [
        "send_custom_message",
        "send_message",
        "send",
        "sendCustomMessage",
        "send_input_message",
        "sendInputMessage",
    ]

    def _maybe_await(res):
        # If the result is awaitable, try to run or schedule it instead of
        # letting it leak a coroutine and produce a RuntimeWarning.
        try:
            if inspect.isawaitable(res):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    # No running loop, run to completion
                    asyncio.run(res)
                else:
                    # If the loop is running in a different thread, use
                    # run_coroutine_threadsafe which is thread-safe.
                    try:
                        import threading

                        if (
                            getattr(loop, "_thread_id", None) is not None
                            and getattr(loop, "_thread_id") != threading.get_ident()
                        ):
                            asyncio.run_coroutine_threadsafe(res, loop)
                            return
                    except Exception:
                        # Fall back to attempting create_task
                        pass

                    # Running loop on this thread: schedule as a task
                    try:
                        loop.create_task(res)
                    except Exception:
                        # Fallbacks if create_task fails
                        try:
                            asyncio.run_coroutine_threadsafe(res, loop)
                        except Exception:
                            try:
                                asyncio.ensure_future(res)
                            except Exception:
                                pass
        except Exception:
            # Best-effort: swallow errors to avoid breaking user apps
            pass

    for m in candidates:
        fn = getattr(session, m, None)
        if callable(fn):
            try:
                # If the method itself is async, call and await/schedule it
                if inspect.iscoroutinefunction(fn):
                    coro = fn(name, payload)
                    _maybe_await(coro)
                    return True

                # Try (name, payload) signature first
                res = fn(name, payload)
                _maybe_await(res)
                return True
            except TypeError:
                # Try a single-dict signature
                try:
                    if inspect.iscoroutinefunction(fn):
                        coro = fn({"type": name, "data": payload})
                        _maybe_await(coro)
                    else:
                        res = fn({"type": name, "data": payload})
                        _maybe_await(res)
                    return True
                except Exception:
                    # give up on this method and try next
                    continue
            except Exception:
                continue
    return False


def update_sidebar(session: Any, menu: list[dict]) -> bool:
    """Request the client replace the sidebar menu.

    - menu: list of dicts like {'text': 'Home', 'href': '#home'}
    """
    payload = {"items": menu}
    return _send_custom_message(session, "bs4dash_update_sidebar", payload)


def update_navbar_tabs(session: Any, nav_id: str, tabs: list[dict]) -> bool:
    """Request the client to update navbar tabs.

    - nav_id: id attribute of the nav container (string)
    - tabs: list of dicts {'id': 'tab1', 'title': 'One', 'href': '#tab1', 'active': True}
    """
    payload = {"nav_id": nav_id, "tabs": tabs}
    return _send_custom_message(session, "bs4dash_update_navs", payload)


def show_controlbar(session: Any) -> bool:
    """Show the controlbar in the client browser for the given Shiny session."""
    return _send_controlbar_message(session, "show")


def hide_controlbar(session: Any) -> bool:
    """Hide the controlbar in the client browser for the given Shiny session."""
    return _send_controlbar_message(session, "hide")


def toggle_controlbar(session: Any) -> bool:
    """Toggle the controlbar in the client browser for the given Shiny session."""
    return _send_controlbar_message(session, "toggle")


def update_sidebar_badges(session: Any, badges: list[dict]) -> bool:
    """Update badges for sidebar links.

    - badges: list of dicts like {'href': '#about', 'badge': '3'}
    """
    payload = {"badges": badges}
    return _send_custom_message(session, "bs4dash_update_sidebar_badges", payload)


def update_navbar_items(session: Any, nav_id: str, items: list[dict]) -> bool:
    """Replace items in a navbar identified by `nav_id`.

    - nav_id: id attribute of the nav container (string)
    - items: list of dicts {'title': 'One', 'href': '#one', 'badge': '5'}
    """
    payload = {"nav_id": nav_id, "items": items}
    return _send_custom_message(session, "bs4dash_update_nav_items", payload)


def update_tab_content(session: Any, tab_id: str, content: str) -> bool:
    """Replace the inner HTML content of a tab pane.

    - tab_id: id of the tab pane to update
    - content: HTML string to set as innerHTML
    """
    payload = {"tab_id": tab_id, "content": content}
    return _send_custom_message(session, "bs4dash_update_tab_content", payload)
