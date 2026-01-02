def test_update_sidebar_uses_session_send_methods():
    from bs4dash_py.server import update_sidebar

    class S:
        def __init__(self):
            self.called = False
            self.args = None

        def send_custom_message(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S()
    menu = [{"text": "Home", "href": "#"}, {"text": "About", "href": "#about"}]
    assert update_sidebar(s, menu) is True
    assert s.called is True
    assert s.args[0] == "bs4dash_update_sidebar"
    assert s.args[1]["items"][0]["text"] == "Home"


def test_async_send_methods_are_awaited():
    from bs4dash_py.server import update_sidebar
    import asyncio

    class SAsync:
        def __init__(self):
            self.called = False
            self.args = None

        async def send_custom_message(self, name, payload):
            # simulate async side-effect
            await asyncio.sleep(0)
            self.called = True
            self.args = (name, payload)

    s = SAsync()
    menu = [{"text": "Foo", "href": "#"}]
    assert update_sidebar(s, menu) is True
    # The implementation may run the coroutine immediately or schedule it on an
    # existing loop; wait briefly for the async handler to complete.
    import time

    deadline = time.time() + 1
    while time.time() < deadline and not s.called:
        time.sleep(0.01)

    assert s.called is True
    assert s.args[0] == "bs4dash_update_sidebar"
    assert s.args[1]["items"][0]["text"] == "Foo"


def test_update_navbar_tabs_sends_message():
    from bs4dash_py.server import update_navbar_tabs

    class S2:
        def __init__(self):
            self.called = False
            self.args = None

        def send(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S2()
    tabs = [{"id": "t1", "title": "One", "href": "#t1", "active": True}]
    assert update_navbar_tabs(s, "navbar1", tabs) is True
    assert s.called is True
    assert s.args[0] == "bs4dash_update_navs"
    assert s.args[1]["nav_id"] == "navbar1"


def test_update_sidebar_badges_adds_badge():
    from bs4dash_py.server import update_sidebar_badges

    class S:
        def __init__(self):
            self.called = False
            self.args = None

        def send_custom_message(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S()
    badges = [{"href": "#about", "badge": "9"}]
    assert update_sidebar_badges(s, badges) is True
    assert s.called is True
    assert s.args[0] == "bs4dash_update_sidebar_badges"
    assert s.args[1]["badges"][0]["badge"] == "9"


def test_update_navbar_items_sends_items():
    from bs4dash_py.server import update_navbar_items

    class S:
        def __init__(self):
            self.called = False
            self.args = None

        def send(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S()
    items = [{"title": "X", "href": "#x", "badge": "1"}]
    assert update_navbar_items(s, "nav-demo", items) is True
    assert s.called is True
    assert s.args[0] == "bs4dash_update_nav_items"
    assert s.args[1]["nav_id"] == "nav-demo"
    assert s.args[1]["items"][0]["badge"] == "1"


def test_update_tab_content_sends_content():
    from bs4dash_py.server import update_tab_content

    class S:
        def __init__(self):
            self.called = False
            self.args = None

        def send_custom_message(self, name, payload):
            self.called = True
            self.args = (name, payload)

    s = S()
    assert update_tab_content(s, "t1", "<p>New</p>") is True
    assert s.called is True
    assert s.args[0] == "bs4dash_update_tab_content"
    assert s.args[1]["tab_id"] == "t1"
    assert "New" in s.args[1]["content"]


def test_running_loop_schedules_coroutine(monkeypatch):
    """Simulate a running event loop by monkeypatching asyncio.get_running_loop
    to return an object whose create_task schedules the coroutine in a
    background thread. The test asserts the coroutine was scheduled and
    eventually executed.
    """
    from bs4dash_py.server import update_sidebar
    import asyncio
    import threading
    import time

    class SAsync:
        def __init__(self):
            self.called = False
            self.args = None

        async def send_custom_message(self, name, payload):
            # simulate work
            await asyncio.sleep(0)
            self.called = True
            self.args = (name, payload)

    class FakeLoop:
        def __init__(self):
            self.scheduled = False

        def create_task(self, coro):
            # mark as scheduled and run the coroutine in a background thread
            self.scheduled = True

            def runner():
                try:
                    asyncio.run(coro)
                except Exception:
                    pass

            t = threading.Thread(target=runner, daemon=True)
            t.start()
            return t

    fake = FakeLoop()

    # monkeypatch asyncio.get_running_loop to return our fake loop
    monkeypatch.setattr(asyncio, "get_running_loop", lambda: fake)

    s = SAsync()
    menu = [{"text": "Bar", "href": "#"}]

    assert update_sidebar(s, menu) is True
    assert fake.scheduled is True

    # wait for background thread to run and set s.called
    deadline = time.time() + 2
    while time.time() < deadline and not s.called:
        time.sleep(0.01)

    assert s.called is True
    assert s.args[0] == "bs4dash_update_sidebar"
    assert s.args[1]["items"][0]["text"] == "Bar"


def test_real_running_loop_schedules_coroutine(monkeypatch):
    """Start a real asyncio loop in a background thread and ensure the
    coroutine is scheduled on that loop using `run_coroutine_threadsafe`.
    """
    from bs4dash_py.server import update_sidebar
    import asyncio
    import threading
    import time

    class SAsync:
        def __init__(self):
            self.called = False
            self.args = None

        async def send_custom_message(self, name, payload):
            await asyncio.sleep(0)
            self.called = True
            self.args = (name, payload)

    loop = asyncio.new_event_loop()

    def run_loop():
        asyncio.set_event_loop(loop)
        loop.run_forever()

    t = threading.Thread(target=run_loop, daemon=True)
    t.start()

    # Ensure the loop is running
    time.sleep(0.05)

    # Monkeypatch get_running_loop to return our background loop so the
    # code path uses the loop and will attempt run_coroutine_threadsafe when
    # create_task fails across threads.
    monkeypatch.setattr(asyncio, "get_running_loop", lambda: loop)

    s = SAsync()
    menu = [{"text": "Baz", "href": "#"}]

    try:
        # Wrap run_coroutine_threadsafe so we can assert it was used and still
        # ensure scheduling goes to the real loop.
        original_run_crt = asyncio.run_coroutine_threadsafe
        called = {"count": 0}

        def _run_crt(coro, target_loop):
            called["count"] += 1
            return original_run_crt(coro, loop)

        monkeypatch.setattr(asyncio, "run_coroutine_threadsafe", _run_crt)

        assert update_sidebar(s, menu) is True

        # Ensure run_coroutine_threadsafe was invoked at least once
        deadline = time.time() + 1
        while time.time() < deadline and called["count"] == 0:
            time.sleep(0.01)
        assert called["count"] > 0

        # Wait up to 3s for the async handler to run on the background loop
        deadline = time.time() + 3
        while time.time() < deadline and not s.called:
            time.sleep(0.01)

        assert s.called is True
        assert s.args[0] == "bs4dash_update_sidebar"
        assert s.args[1]["items"][0]["text"] == "Baz"
    finally:
        # Stop background loop and join thread
        loop.call_soon_threadsafe(loop.stop)
        t.join(timeout=1)
