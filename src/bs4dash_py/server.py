import asyncio
import inspect
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

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
- If scheduling fails (different thread), `asyncio.run_coroutine_threadsafe`
  will be attempted as a fallback.

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

    def _schedule_awaitable(res: Any) -> None:
        """Schedule or run an awaitable/coroutine in a robust, best-effort way.

        The function attempts scheduling in the following order:
        1. If there is no running loop, execute the coroutine to completion
           using `asyncio.run`.
        2. If a running loop exists on another thread, prefer
           `asyncio.run_coroutine_threadsafe`.
        3. If the loop appears to be same-thread, attempt `loop.create_task`.
        4. Fall back to `asyncio.ensure_future` as a last resort.

        All exceptions are caught and logged at debug level; this function is
        intentionally conservative to avoid breaking user apps when scheduling
        fails in uncommon runtime environments.
        """
        try:
            if not inspect.isawaitable(res):
                return
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # No running loop: execute to completion
                asyncio.run(res)
                return

            # If the loop appears to be running on a different thread, prefer
            # the thread-safe scheduling primitive `run_coroutine_threadsafe`.
            try:
                import threading

                loop_thread_id = getattr(loop, "_thread_id", None)
                if (
                    loop_thread_id is not None
                    and loop_thread_id != threading.get_ident()
                ):
                    try:
                        asyncio.run_coroutine_threadsafe(res, loop)
                        return
                    except Exception:
                        # Fall through to other scheduling attempts
                        pass
            except Exception:
                # Ignore inspection errors and continue
                pass

            # Try scheduling on the running loop (same-thread optimistic path)
            try:
                loop.create_task(res)
                return
            except Exception:
                # Could be a scheduling failure; try thread-safe scheduling as a fallback
                try:
                    asyncio.run_coroutine_threadsafe(res, loop)
                    return
                except Exception:
                    pass

            # Final fallback
            try:
                asyncio.ensure_future(res)
            except Exception:
                logger.debug("Failed to schedule awaitable", exc_info=True)
        except Exception:
            # Best-effort: don't let scheduling errors propagate
            logger.debug("Unexpected error while scheduling awaitable", exc_info=True)

    for m in candidates:
        fn = getattr(session, m, None)
        if callable(fn):
            try:
                # If the method itself is async, call and schedule it
                if inspect.iscoroutinefunction(fn):
                    coro = fn(name, payload)
                    _schedule_awaitable(coro)
                    return True

                # Try (name, payload) signature first
                try:
                    res = fn(name, payload)
                    _schedule_awaitable(res)
                    return True
                except TypeError:
                    # Try a single-dict signature
                    try:
                        res = fn({"type": name, "data": payload})
                        _schedule_awaitable(res)
                        return True
                    except Exception:
                        # give up on this method and try next
                        continue
            except Exception:
                # Log at debug level to aid troubleshooting while remaining tolerant
                logger.debug("Error calling session send method %s", m, exc_info=True)
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


def update_sidebar_active(session: Any, target: str) -> bool:
    """Set the active sidebar item on the client.

    - target: either a selector (e.g., "a.nav-link[href='#about']") or an href like
      "#about" (the client will look up by href if an href string is passed).
    Example: `update_sidebar_active(session, '#about')` or
             `update_sidebar_active(session, "a.nav-link[href='#about']")`.
    """
    payload = {"target": target}
    return _send_custom_message(session, "bs4dash_update_sidebar_active", payload)


def update_navbar_items(session: Any, nav_id: str, items: list[dict]) -> bool:
    """Replace items in a navbar identified by `nav_id`.

    - nav_id: id attribute of the nav container (string)
    - items: list of dicts {'title': 'One', 'href': '#one', 'badge': '5'}
    """
    payload = {"nav_id": nav_id, "items": items}
    return _send_custom_message(session, "bs4dash_update_nav_items", payload)


def add_navbar_item(session: Any, nav_id: str, item: dict) -> bool:
    """Add a single item to a navbar.

    - nav_id: id of the nav container
    - item: dict with keys like {'title': 'New', 'href': '#new', 'badge': '1'}
    """
    payload = {"nav_id": nav_id, "item": item}
    return _send_custom_message(session, "bs4dash_add_nav_item", payload)


def remove_navbar_item(session: Any, nav_id: str, href: str) -> bool:
    """Remove a navbar item matching the given href from the navbar.

    - href: the href string to match (e.g., '#old')
    """
    payload = {"nav_id": nav_id, "href": href}
    return _send_custom_message(session, "bs4dash_remove_nav_item", payload)


def update_navbar_badge(
    session: Any, nav_id: str, href: str, badge: Optional[str]
) -> bool:
    """Update (or remove) a badge on a navbar item.

    - badge: string to set, or None to remove the badge
    """
    payload = {"nav_id": nav_id, "href": href, "badge": badge}
    return _send_custom_message(session, "bs4dash_update_nav_badge", payload)


def update_tab_content(session: Any, tab_id: str, content: str) -> bool:
    """Replace the inner HTML content of a tab pane.

    - tab_id: id of the tab pane to update
    - content: HTML string to set as innerHTML
    """
    payload = {"tab_id": tab_id, "content": content}
    return _send_custom_message(session, "bs4dash_update_tab_content", payload)
