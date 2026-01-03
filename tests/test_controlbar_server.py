import types

from bs4dash_py.server import (
    _send_controlbar_message,
    hide_controlbar,
    show_controlbar,
    toggle_controlbar,
)


class DummySession:
    def __init__(self):
        self.calls = []

    def send_custom_message(self, name, payload):
        self.calls.append((name, payload))


def test_send_controlbar_message_uses_send_custom_message():
    s = DummySession()
    assert _send_controlbar_message(s, "show") is True
    assert s.calls == [("bs4dash_controlbar", {"action": "show"})]


def test_show_hide_toggle_helpers():
    s = DummySession()
    assert show_controlbar(s) is True
    assert hide_controlbar(s) is True
    assert toggle_controlbar(s) is True


def test_fallback_to_other_signatures():
    # Simulate a session with a single-arg send method
    called = {}

    def send(payload):
        called["payload"] = payload

    s = types.SimpleNamespace(send=send)
    assert _send_controlbar_message(s, "hide") is True
    assert "payload" in called
    assert called["payload"].get("type") == "bs4dash_controlbar"
    assert called["payload"].get("data") == {"action": "hide"}
