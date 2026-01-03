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
        pytest.fail(f"Themed example did not start: {last_err}")
    return port, proc


def test_bslib_conversion_applies(playwright_page):
    script = Path("examples") / "mvp_shiny_from_bslib.py"
    assert script.exists()
    port, proc = _start(str(script))
    page = playwright_page
    page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

    def primary_bg():
        return page.evaluate(
            "() => getComputedStyle(document.querySelector('.small-box.bg-primary')).backgroundColor"
        )

    baseline = primary_bg()

    # Apply dark converted theme and check it changes
    page.click("#apply-dark")
    page.wait_for_timeout(500)
    new_bg = primary_bg()
    assert new_bg and new_bg != baseline

    # Apply flatly via bootswatch href (vendored or CDN)
    page.click("#apply-flat-bs")
    page.wait_for_timeout(800)
    has_link = page.evaluate(
        "() => !!document.getElementById('bootswatch-link') && document.getElementById('bootswatch-link').href.includes('flatly')"
    )
    assert has_link

    try:
        proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
