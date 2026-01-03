def test_add_navbar_item_sends_message():
    from bs4dash_py.server import add_navbar_item

    class S:
        def __init__(self):
            self.called = False
            self.args = None

        def send(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S()
    item = {"title": "New", "href": "#new", "badge": "7"}
    assert add_navbar_item(s, "demo-nav", item) is True
    assert s.called is True
    assert s.args[0] == "bs4dash_add_nav_item"
    assert s.args[1]["item"]["title"] == "New"


def test_remove_navbar_item_sends_message():
    from bs4dash_py.server import remove_navbar_item

    class S:
        def __init__(self):
            self.called = False
            self.args = None

        def send(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S()
    assert remove_navbar_item(s, "demo-nav", "#old") is True
    assert s.called is True
    assert s.args[0] == "bs4dash_remove_nav_item"
    assert s.args[1]["href"] == "#old"


def test_update_navbar_badge_sends_message():
    from bs4dash_py.server import update_navbar_badge

    class S:
        def __init__(self):
            self.called = False
            self.args = None

        def send_custom_message(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S()
    assert update_navbar_badge(s, "demo-nav", "#one", "5") is True
    assert s.called is True
    assert s.args[0] == "bs4dash_update_nav_badge"
    assert s.args[1]["badge"] == "5"
