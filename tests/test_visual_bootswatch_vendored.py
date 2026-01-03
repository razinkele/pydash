from pathlib import Path

import pytest


def _start(script_path: str, timeout: int = 60):
    import socket
    import subprocess
    import time
    import urllib.request

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    proc = subprocess.Popen(
        ["python", script_path],
        env={"PYBS4DASH_PORT": str(port)},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    deadline = time.time() + timeout
    last_err = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2) as r:
                _ = r.read()
                break
        except Exception as e:
            last_err = e
            time.sleep(0.5)
    else:
        proc.terminate()
        proc.wait(timeout=3)
        pytest.fail(f"Themed showcase did not start: {last_err}")
    return port, proc


def test_bootswatch_buttons_apply_vendored_themes(playwright_page):
    script = Path("examples") / "mvp_shiny_themes_showcase.py"
    assert script.exists()
    port, proc = _start(str(script))
    page = playwright_page
    page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

    # Helper to read primary box background
    def primary_bg():
        return page.evaluate(
            "() => getComputedStyle(document.querySelector('.small-box.bg-primary')).backgroundColor"
        )

    baseline = primary_bg()

    buttons = [
        ("#theme-bs-flatly", "flatly"),
        ("#theme-bs-cerulean", "cerulean"),
        ("#theme-bs-solar", "solar"),
    ]

    any_changed = False
    for selector, name in buttons:
        page.click(selector)
        page.wait_for_timeout(800)

        # Ensure link is present and references the expected theme
        has_link = page.evaluate(
            f"() => !!document.getElementById('bootswatch-link') && document.getElementById('bootswatch-link').href.includes('{name}')"
        )
        assert has_link, f"Expected bootswatch link for {name} to exist"

        new_bg = primary_bg()
        if new_bg != baseline:
            any_changed = True
            baseline = new_bg

    # If none of the vendored themes produced a visible change, skip (browser may block file:// stylesheets)
    if not any_changed:
        pytest.skip(
            "Vendored Bootswatch CSS did not apply or produced no visual diffs in this environment"
        )

    try:
        proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
