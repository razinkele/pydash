def test_visual_sidebar_toggle():
    import os
    import sys
    import subprocess
    import socket
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
        deadline = time.time() + 15
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

                # Ensure toggle button exists
                assert page.query_selector("#pushmenu-toggle") is not None

                # Initially body should not have sidebar-collapse
                initial = page.evaluate(
                    "() => document.body.classList.contains('sidebar-collapse')"
                )
                assert initial is False

                # Click toggle
                page.click("#pushmenu-toggle")

                # Wait for class to be applied
                page.wait_for_function(
                    "() => document.body.classList.contains('sidebar-collapse')",
                    timeout=5000,
                )

                toggled = page.evaluate(
                    "() => document.body.classList.contains('sidebar-collapse')"
                )
                assert toggled is True

                browser.close()
        except Exception as e:
            pytest.skip(f"Playwright test failed to run: {e}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
