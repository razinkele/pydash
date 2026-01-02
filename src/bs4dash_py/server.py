from typing import Any


def _send_controlbar_message(session: Any, action: str = "toggle") -> bool:
    """Send a controlbar message to the client using the Shiny session.

    Tries a few common method names for sending custom messages so this works
    across multiple Shiny Session-like implementations.
    """
    # Normalize action
    action = action or "toggle"

    message_name = "bs4dash_controlbar"
    payload = {"action": action}

    # Candidate method names to try on session objects
    candidates = [
        "send_custom_message",
        "send_message",
        "send",
        "sendCustomMessage",
        "send_input_message",
        "sendInputMessage",
    ]

    for name in candidates:
        fn = getattr(session, name, None)
        if callable(fn):
            try:
                # Try (name, payload) signature first
                fn(message_name, payload)
                return True
            except TypeError:
                # Try a single-dict signature
                try:
                    fn({"type": message_name, "data": payload})
                    return True
                except Exception:
                    # give up on this method and try next
                    continue
            except Exception:
                continue

    # nothing worked
    return False


def show_controlbar(session: Any) -> bool:
    """Show the controlbar in the client browser for the given Shiny session."""
    return _send_controlbar_message(session, "show")


def hide_controlbar(session: Any) -> bool:
    """Hide the controlbar in the client browser for the given Shiny session."""
    return _send_controlbar_message(session, "hide")


def toggle_controlbar(session: Any) -> bool:
    """Toggle the controlbar in the client browser for the given Shiny session."""
    return _send_controlbar_message(session, "toggle")
