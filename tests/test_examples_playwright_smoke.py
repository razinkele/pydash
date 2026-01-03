import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

# Import playwright lazily so tests that don't have it installed can be skipped
pytest.importorskip("playwright.sync_api")
from playwright.sync_api import sync_playwright  # noqa: E402


def _start_example_for_test(port: int):
    env = os.environ.copy()
    env["PYBS4DASH_PORT"] = str(port)
    # use local assets to avoid CDN reliance in CI
    env["PYBS4DASH_BOOTSWATCH_SRC"] = "local"
    env["PYBS4DASH_ADMINLTE"] = str(Path("tests/assets/adminlte.min.css").resolve())
    env["PYBS4DASH_ADMINLTE_JS"] = str(Path("tests/assets/adminlte.min.js").resolve())

    proc = subprocess.Popen(
        [sys.executable, "examples/mvp_shiny_from_bslib.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc


def _wait_for_port(port: int, timeout: int = 30):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2) as _:
                return True
        except Exception as e:
            last = e
            time.sleep(0.5)
    raise RuntimeError(f"Server did not respond in time: {last}")


def test_examples_playwright_smoke(tmp_path):
    port = 8766
    proc = _start_example_for_test(port)
    try:
        _wait_for_port(port, timeout=20)
        # Run Playwright against the example and run a minimal axe audit
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"http://127.0.0.1:{port}/", wait_until="domcontentloaded")

            # Ensure page loaded
            _ = page.title().lower() or page.content()

            # Add axe (will be intercepted by fixture routing in conftest if needed)
            axe_url = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.3/axe.min.js"
            page.add_script_tag(url=axe_url)

            # run axe
            axe = page.evaluate(
                "async () => { const r = await axe.run(); return {violations: r.violations.map(v=>({id:v.id, impact:v.impact}))}; }"
            )
            violations = axe.get("violations") if isinstance(axe, dict) else []
            critical = [v for v in violations if v.get("impact") == "critical"]
            if critical:
                # save some debug info to stdout to help CI triage
                print("axe failures:", critical)
            assert not critical, f"Critical accessibility violations: {critical}"

            context.close()
            browser.close()
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
