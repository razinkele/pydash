import subprocess
import sys
import time
import urllib.request

proc = subprocess.Popen(
    [sys.executable, "examples/mvp_shiny.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
try:
    for _ in range(60):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/") as r:
                _ = r.read()
                break
        except Exception:
            time.sleep(0.5)
    else:
        print("server not started", proc.stderr.read().decode(), file=sys.stderr)
        proc.terminate()
        proc.wait()
        sys.exit(1)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/")
        time.sleep(1)
        n = page.evaluate(
            "() => document.querySelectorAll('ul.nav.nav-pills.nav-sidebar.flex-column > li.nav-item[role='menuitem']').length"
        )
        print("menuitems count:", n)
        sample = page.evaluate(
            "() => (document.querySelector('ul.nav.nav-pills.nav-sidebar.flex-column > li.nav-item')||{}).outerHTML"
        )
        print("sample:", sample[:400])
        browser.close()
finally:
    proc.terminate()
    proc.wait()
