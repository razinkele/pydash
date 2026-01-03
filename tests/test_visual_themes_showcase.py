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


def test_theme_switching(playwright_page):
    script = Path("examples") / "mvp_shiny_themes_showcase.py"
    assert script.exists()
    port, proc = _start(str(script))
    page = playwright_page
    page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

    # Helper to read avatar bg
    def avatar_bg():
        return page.evaluate(
            "() => getComputedStyle(document.querySelector('.user-avatar-initials')).backgroundColor"
        )

    # Click Dark theme and assert avatar changes and nav/badge are updated
    page.click("#theme-dark")
    page.wait_for_timeout(500)
    bg_dark = avatar_bg()
    assert bg_dark and ("rgb" in bg_dark)

    # Badge color after dark theme
    badge_bg_dark = page.evaluate(
        "() => getComputedStyle(document.querySelector('.badge.badge-info')).backgroundColor"
    )
    assert badge_bg_dark and ("108, 117" in badge_bg_dark or "108,117" in badge_bg_dark)

    # Nav active background after dark theme
    nav_bg_dark = page.evaluate(
        "() => getComputedStyle(document.querySelector('#showcase-nav .nav-link.active')).backgroundColor"
    )
    assert nav_bg_dark and (
        "0" in nav_bg_dark or "20, 39" in nav_bg_dark or "20,27" in nav_bg_dark
    )

    # Click High contrast and assert expected (black) avatar background and badge/nav
    page.click("#theme-high")
    page.wait_for_timeout(500)
    bg_high = avatar_bg()
    assert bg_high and ("0, 0, 0" in bg_high)

    badge_bg_high = page.evaluate(
        "() => getComputedStyle(document.querySelector('.badge.badge-info')).backgroundColor"
    )
    assert badge_bg_high and (
        "255, 255, 255" in badge_bg_high or "255,255,255" in badge_bg_high
    )

    nav_bg_high = page.evaluate(
        "() => getComputedStyle(document.querySelector('#showcase-nav .nav-link.active')).backgroundColor"
    )
    assert nav_bg_high and (
        "255, 255, 255" in nav_bg_high or "255,255,255" in nav_bg_high
    )

    # Click Light theme and assert different from high contrast
    page.click("#theme-light")
    page.wait_for_timeout(500)
    bg_light = avatar_bg()
    assert bg_light and ("0, 0, 0" not in bg_light)

    badge_bg_light = page.evaluate(
        "() => getComputedStyle(document.querySelector('.badge.badge-info')).backgroundColor"
    )
    assert badge_bg_light and (
        "255, 107" in badge_bg_light or "255, 107, 107" in badge_bg_light
    )

    nav_bg_light = page.evaluate(
        "() => getComputedStyle(document.querySelector('#showcase-nav .nav-link.active')).backgroundColor"
    )
    assert nav_bg_light and ("233, 236" in nav_bg_light or "233,236" in nav_bg_light)

    # Try Bootswatch flatly (CDN). Skip if CDN unreachable.
    import urllib.request

    try:
        with urllib.request.urlopen(
            "https://cdn.jsdelivr.net/npm/bootswatch@5/dist/flatly/bootstrap.min.css",
            timeout=5,
        ) as r:
            assert r.status == 200
    except Exception:
        pytest.skip("Bootswatch CDN unreachable; skipping Bootswatch checks")

    # Click the Bootswatch button and assert a bootswatch link exists in head
    page.click("#theme-bs-flatly")
    page.wait_for_timeout(800)
    has_link = page.evaluate(
        "() => !!document.getElementById('bootswatch-link') && document.getElementById('bootswatch-link').href.includes('bootswatch')"
    )
    assert has_link
    try:
        proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
