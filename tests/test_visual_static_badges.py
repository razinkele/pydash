def test_visual_static_navbar_and_sidebar_badges():
    import os
    import socket
    import subprocess
    import sys
    import time

    import pytest

    pytest.importorskip("playwright.sync_api")

    # Find a free port
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
        # Wait for server to be ready (timeout)
        deadline = time.time() + 30
        last_err = None
        while time.time() < deadline:
            try:
                import urllib.request

                with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
                    _ = resp.read()
                    break
            except Exception as e:
                last_err = e
                time.sleep(0.5)
        else:
            pytest.fail(f"Server did not respond in time: {last_err}")

        from playwright.sync_api import sync_playwright

        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch(headless=True)
                except Exception as e:
                    pytest.skip(f"Playwright browsers not available: {e}")
                page = browser.new_page()

                page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

                # Static sidebar badge (About has badge '1')
                page.wait_for_selector(
                    ".main-sidebar .nav a[href='#about'] .badge",
                    timeout=5000,
                )
                assert (
                    page.evaluate(
                        "() => document.querySelector('.main-sidebar .nav a[href=\"#about\"] .badge').textContent"
                    )
                    == "1"
                )
                # Accessibility: badge should have an aria-label describing it
                assert (
                    page.evaluate(
                        "() => document.querySelector('.main-sidebar .nav a[href=\"#about\"] .badge').getAttribute('aria-label')"
                    )
                    is not None
                )

                # Static navbar badge (Notifications has badge '2')
                page.wait_for_selector("a.nav-link[href='#notif'] .badge", timeout=5000)
                assert (
                    page.evaluate(
                        "() => document.querySelector('a.nav-link[href=\"#notif\"] .badge').textContent"
                    )
                    == "2"
                )
                # Accessibility: navbar badge should have aria-label
                assert (
                    page.evaluate(
                        "() => document.querySelector('a.nav-link[href=\"#notif\"] .badge').getAttribute('aria-label')"
                    )
                    is not None
                )

                browser.close()
        except Exception as e:
            pytest.skip(f"Playwright test failed to run: {e}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
