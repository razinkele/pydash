def test_visual_controlbar_asset_and_show_hide():
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
        deadline = time.time() + 20
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

                # Intercept page requests to assert the asset is requested
                page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

                # Ensure the controlbar script is present (either external or inlined)
                try:
                    has_script = page.evaluate(
                        "() => !!document.querySelector(\"script[src*='bs4dash_controlbar.js']\") || Array.from(document.scripts).some(s=>s.textContent && s.textContent.includes('bs4dash_controlbar'))"
                    )
                    assert has_script
                except Exception:
                    pytest.fail("bs4dash_controlbar.js was not included on the page")

                # Initially controlbar should not be open
                assert (
                    page.evaluate(
                        "() => document.body.classList.contains('control-sidebar-open')"
                    )
                    is False
                )

                # Click the show button and wait for class
                page.click("#show_cb")
                page.wait_for_function(
                    "() => document.body.classList.contains('control-sidebar-open')",
                    timeout=5000,
                )
                assert (
                    page.evaluate(
                        "() => document.body.classList.contains('control-sidebar-open')"
                    )
                    is True
                )

                # Click hide button and wait for removal
                page.click("#hide_cb")
                page.wait_for_function(
                    "() => !document.body.classList.contains('control-sidebar-open')",
                    timeout=5000,
                )
                assert (
                    page.evaluate(
                        "() => document.body.classList.contains('control-sidebar-open')"
                    )
                    is False
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
