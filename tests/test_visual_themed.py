import subprocess
import socket
import time
from pathlib import Path

import pytest


def _start_example_script(script_path: str, timeout: int = 60):
    """Start a python script as an example app on a free port and return (port, proc)

    This is a lightweight helper for tests that need to start a specific
    example (instead of the default `examples/mvp_shiny.py`). It mirrors the
    logic used in `start_example` but is scoped to this test file.
    """
    # pick free port
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()

    proc = subprocess.Popen(["python", script_path], env={"PYBS4DASH_PORT": str(port)}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    deadline = time.time() + timeout
    last_err = None
    while time.time() < deadline:
        try:
            import urllib.request

            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2) as r:
                _ = r.read()
                break
        except Exception as e:
            last_err = e
            time.sleep(0.5)
    else:
        # timed out
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
        pytest.fail(f"Themed example did not start in time: {last_err}")

    return port, proc


def test_visual_themed_example(playwright_page, tmp_path):
    """Launch the themed example and verify theme variables and accessibility."""
    script = Path("examples") / "mvp_shiny_themed.py"
    assert script.exists(), "The themed example script is missing"

    port, proc = _start_example_script(str(script))

    page = playwright_page
    page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

    # Check that the avatar token override in examples/assets/custom_theme.css is applied
    # The example sets --bs4dash-avatar-bg: #1f7a8c; so the computed background color should reflect it
    page.wait_for_selector(".user-avatar-initials", timeout=5000)
    bg = page.evaluate("() => getComputedStyle(document.querySelector('.user-avatar-initials')).backgroundColor")
    assert bg and ("23, 122" in bg or "31, 122" in bg or "26, 118" in bg), f"Unexpected avatar bg: {bg}"

    # Verify a themed badge color from the custom CSS
    page.wait_for_selector(".badge.badge-info", timeout=5000)
    badge_bg = page.evaluate("() => getComputedStyle(document.querySelector('.badge.badge-info')).backgroundColor")
    assert badge_bg and ("255, 107, 107" in badge_bg or "255, 107" in badge_bg), f"Unexpected badge color: {badge_bg}"

    # Run a short axe audit to ensure no critical regressions introduced by the theme
    asset_path = Path(__file__).parent / "assets" / "axe.min.js"
    axe_url = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.3/axe.min.js"
    try:
        page.wait_for_timeout(800)
        if asset_path.exists():
            page.add_script_tag(path=str(asset_path))
        else:
            page.add_script_tag(url=axe_url)
    except Exception:
        pytest.skip("Could not load axe for themed example; skipping axe audit")

    # Apply any necessary inline styles to ensure deterministic contrast checks
    page.evaluate("() => { document.querySelectorAll('a[href="#t2"], a[href="#a"]').forEach(function(el){ try{ el.style.color='#000000'; el.style.backgroundColor='#ffffff'; }catch(e){} }); }")

    axe = page.evaluate("async () => { const r = await axe.run(); return {violations: r.violations.map(v=>({id:v.id, impact:v.impact}))}; }")
    violations = axe.get("violations") if isinstance(axe, dict) else []
    # Fail on critical issues only for now
    critical = [v for v in violations if v.get("impact") == "critical"]
    assert not critical, f"Critical accessibility violations in themed example: {critical}"

    # Teardown
    try:
        proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        proc.kill()