from pathlib import Path

import pytest


def _start(script_path: str, timeout: int = 60, env_overrides: dict | None = None):
    import os
    import socket
    import subprocess
    import time
    import urllib.request

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    import sys

    env = os.environ.copy()
    env["PYBS4DASH_PORT"] = str(port)
    if env_overrides:
        env.update(env_overrides)

    proc = subprocess.Popen(
        [sys.executable, script_path],
        env=env,
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

    # Prefer local vendored AdminLTE assets in CI to avoid CDN/DNS flakiness
    assets_dir = Path(__file__).parent / "assets"
    css_path = str((assets_dir / "adminlte.min.css").resolve())
    js_path = str((assets_dir / "adminlte.min.js").resolve())

    port, proc = _start(
        str(script),
        env_overrides={
            "PYBS4DASH_ADMINLTE": css_path,
            "PYBS4DASH_ADMINLTE_JS": js_path,
        },
    )
    page = playwright_page
    page.goto(f"http://127.0.0.1:{port}/", timeout=10000, wait_until="domcontentloaded")

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
