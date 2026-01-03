def test_visual_sidebar_active_update():
    import os
    import socket
    import subprocess
    import sys
    import time

    import pytest

    pytest.importorskip("playwright.sync_api")

    # Start example app
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()

    env = os.environ.copy()
    env["PYBS4DASH_PORT"] = str(port)

    proc = subprocess.Popen(
        [sys.executable, "examples/mvp_shiny.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Wait for server
        deadline = time.time() + 30
        while time.time() < deadline:
            try:
                import urllib.request

                with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
                    _ = resp.read()
                    break
            except Exception:
                time.sleep(0.5)
        else:
            pytest.fail("Server did not start in time")

        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                pytest.skip(f"Playwright browsers not available: {e}")
            page = browser.new_page()

            page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

            # Ensure About initially has a badge but is not active
            page.wait_for_selector(
                ".main-sidebar a.nav-link[href='#about']", timeout=5000
            )
            assert "active" not in page.evaluate(
                "() => document.querySelector('.main-sidebar a.nav-link[href=\"#about\"]').className"
            )

            # Click the Activate About button which triggers server helper
            page.click("#bs_activate_about")

            # Wait for the sidebar link to become active
            page.wait_for_selector(
                ".main-sidebar a.nav-link[href='#about'].active", timeout=5000
            )
            assert "active" in page.evaluate(
                "() => document.querySelector('.main-sidebar a.nav-link[href=\"#about\"]').className"
            )

            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
