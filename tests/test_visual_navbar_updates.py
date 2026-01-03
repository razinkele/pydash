def test_visual_navbar_add_remove_and_badge():
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

            # Add nav item
            page.click("#bs_add_nav_item")
            page.wait_for_selector("#demo-navbar a.nav-link[href='#new']", timeout=5000)
            # The link may contain a badge element; ensure the visible label is the link text node and the badge has the expected text
            link_text = page.evaluate(
                "() => (function(el){ return (el && el.childNodes && el.childNodes[0]) ? el.childNodes[0].textContent.trim() : (el ? el.textContent.trim() : ''); })(document.querySelector('#demo-navbar a.nav-link[href=\"#new\"]'))"
            )
            assert link_text == "New"
            # If a badge exists, verify it contains the expected number
            if page.query_selector("#demo-navbar a.nav-link[href='#new'] .badge"):
                assert (
                    page.evaluate(
                        "() => document.querySelector('#demo-navbar a.nav-link[href=\"#new\"] .badge').textContent"
                    )
                    == "7"
                )

            # Ensure navbar contains '#one' item (update navbar items), then update badge on '#one'
            page.click("#bs_update_navbar_items")
            page.wait_for_selector("#demo-navbar a.nav-link[href='#one']", timeout=5000)
            page.click("#bs_update_nav_badge")
            page.wait_for_selector(
                "#demo-navbar a.nav-link[href='#one'] .badge", timeout=5000
            )
            assert (
                page.evaluate(
                    "() => document.querySelector('#demo-navbar a.nav-link[href=\"#one\"] .badge').textContent"
                )
                == "9"
            )

            # Remove the new nav item
            page.click("#bs_remove_nav_item")
            # Wait until the link is gone
            page.wait_for_function(
                "() => document.querySelector('#demo-navbar a.nav-link[href=\"#new\"]') === null",
                timeout=5000,
            )

            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
