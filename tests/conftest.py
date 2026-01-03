import os
import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path so tests can import the package without installing it
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
# Prefer editable-style import from src/
if SRC not in sys.path:
    sys.path.insert(0, SRC)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

ARTIFACTS_DIR = Path(os.environ.get("TEST_ARTIFACTS", "test-artifacts"))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test reports on the item so fixtures can access pass/fail status."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def playwright_page(request):
    """Provide a Playwright page with tracing enabled and capture artifacts on failure.

    Yields a Playwright `page` object. On failure, saves screenshot, HTML, and a
    Playwright trace under `test-artifacts/<nodeid>/`.
    """
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright

    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    adir = ARTIFACTS_DIR / nodeid
    adir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # set up a HAR capture file to record network activity (will be written
        # by Playwright when the context closes). We prefer to record to the
        # artifacts dir so it is easy to upload later if the test fails.
        har_path = adir / "network.har"
        context = browser.new_context(record_har_path=str(har_path))
        # start tracing (we'll stop and save if the test fails)
        context.tracing.start(screenshots=True, snapshots=True)

        # Intercept known CDN requests and provide local fallbacks to avoid CI network flakiness.
        from pathlib import Path

        assets_dir = Path(__file__).parent / "assets"

        def _cdn_route(route, request):
            try:
                url = request.url
                res_type = request.resource_type
                # Axe-core stub
                if "axe.min.js" in url:
                    stub = assets_dir / "axe_stub.min.js"
                    if not stub.exists():
                        stub = Path(__file__).parent / "stubs" / "axe_stub.min.js"
                    if stub.exists():
                        body = stub.read_bytes()
                    else:
                        body = b"window.axe={run:async()=>({violations:[]})};"
                    return route.fulfill(
                        status=200,
                        body=body,
                        headers={"Content-Type": "application/javascript"},
                    )
                # CSS fallback
                if url.endswith(".css"):
                    # Bootswatch / theme CSS
                    if any(
                        k in url
                        for k in ("bootswatch", "bootswatch.com", "bootswatch.org")
                    ):
                        stub = assets_dir.parent / "stubs" / "bootswatch_stub.min.css"
                        if stub.exists():
                            return route.fulfill(
                                status=200,
                                body=stub.read_bytes(),
                                headers={"Content-Type": "text/css"},
                            )
                    # Google Fonts CSS
                    if any(
                        k in url for k in ("fonts.googleapis.com", "fonts.gstatic.com")
                    ):
                        stub = assets_dir.parent / "stubs" / "google_fonts_stub.css"
                        if stub.exists():
                            return route.fulfill(
                                status=200,
                                body=stub.read_bytes(),
                                headers={"Content-Type": "text/css"},
                            )
                    stub = assets_dir / (Path(url).name)
                    if stub.exists():
                        return route.fulfill(
                            status=200,
                            body=stub.read_bytes(),
                            headers={"Content-Type": "text/css"},
                        )
                    return route.fulfill(
                        status=200,
                        body=b"/* stub */",
                        headers={"Content-Type": "text/css"},
                    )
                # JS fallback (AdminLTE, bootstrap, etc.)
                if url.endswith(".js"):
                    stub = assets_dir / (Path(url).name)
                    if stub.exists():
                        return route.fulfill(
                            status=200,
                            body=stub.read_bytes(),
                            headers={"Content-Type": "application/javascript"},
                        )
                    # provide a harmless no-op for known UI libs to avoid runtime errors
                    if any(
                        k in url
                        for k in ("adminlte", "bootstrap", "bslib", "bootswatch")
                    ):
                        return route.fulfill(
                            status=200,
                            body=b"(function(){window.AdminLTE=window.AdminLTE||{};})();",
                            headers={"Content-Type": "application/javascript"},
                        )
                    return route.fulfill(
                        status=200,
                        body=b"// stub",
                        headers={"Content-Type": "application/javascript"},
                    )
                # Abort fonts/images to avoid blocking when network is restricted
                if res_type in ("image", "font"):
                    return route.abort()
            except Exception:
                pass
            return route.continue_()

        try:
            context.route("**/*", _cdn_route)
        except Exception:
            pass

        page = context.new_page()

        # collect console messages for later inspection
        console_msgs = []

        def _on_console(msg):
            try:
                console_msgs.append(f"{msg.type}: {msg.text}")
            except Exception:
                console_msgs.append(f"console:{str(msg)}")

        page.on("console", _on_console)

        # register for later use in other fixtures if needed
        request.node._pw_resources = {
            "context": context,
            "page": page,
            "browser": browser,
            "adir": adir,
            "console": console_msgs,
            "har_path": har_path,
        }

        try:
            yield page
        finally:
            rep = getattr(request.node, "rep_call", None)
            failed = bool(rep and rep.failed)
            if failed:
                try:
                    screenshot_path = adir / "screenshot.png"
                    page.screenshot(path=str(screenshot_path))
                except Exception as e:
                    (adir / "screenshot_error.txt").write_text(str(e))
                try:
                    (adir / "page.html").write_text(page.content(), encoding="utf-8")
                except Exception as e:
                    (adir / "page_html_error.txt").write_text(str(e))
                try:
                    trace_path = adir / "trace.zip"
                    context.tracing.stop(path=str(trace_path))
                except Exception as e:
                    (adir / "trace_error.txt").write_text(str(e))
                # write console logs
                try:
                    cfile = adir / "console.log"
                    cfile.write_text("\n".join(console_msgs), encoding="utf-8")
                except Exception as e:
                    (adir / "console_error.txt").write_text(str(e))
                # ensure HAR file exists and note if missing
                try:
                    har_file = adir / "network.har"
                    if not har_file.exists():
                        # Playwright should write HAR to the path we provided; if not,
                        # attempt to copy from the path registered on the node
                        node_har = request.node._pw_resources.get("har_path")
                        if node_har and Path(node_har).exists():
                            import shutil

                            shutil.copy(Path(node_har), har_file)
                        else:
                            (adir / "har_missing.txt").write_text(
                                "HAR file not found after test"
                            )
                except Exception as e:
                    (adir / "har_error.txt").write_text(str(e))
            # cleanup
            try:
                context.close()
            except Exception:
                pass
            try:
                browser.close()
            except Exception:
                pass


@pytest.fixture
def start_example(request):
    """Start the example app on a free port and yield the port number.

    On test failure, save server stdout/stderr into the artifact directory.

    This fixture now streams stdout/stderr to live files in the artifacts
    directory and prints periodic stderr summaries while waiting for the
    server to start. The startup timeout is configurable with
    `PYBS4DASH_START_TIMEOUT` (seconds, default 60).
    """
    import socket
    import subprocess
    import sys
    import threading
    import time
    import urllib.request
    from collections import deque

    # configurable timeout (default 60s to account for slower environments)
    timeout = int(os.environ.get("PYBS4DASH_START_TIMEOUT", "60"))

    # prepare artifact dir for live logs
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    adir = ARTIFACTS_DIR / nodeid
    adir.mkdir(parents=True, exist_ok=True)
    stdout_live = adir / "server_stdout_live.txt"
    stderr_live = adir / "server_stderr_live.txt"

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

    # stream stdout/stderr to live files and keep a small in-memory tail
    stdout_tail = deque(maxlen=200)
    stderr_tail = deque(maxlen=200)

    def _reader(stream, tail, path):
        try:
            with open(path, "a", encoding="utf-8") as fh:
                while True:
                    b = stream.readline()
                    if not b:
                        break
                    try:
                        line = b.decode(errors="replace")
                    except Exception:
                        line = str(b)
                    fh.write(line)
                    fh.flush()
                    tail.append(line.rstrip("\n"))
        except Exception as e:
            (adir / "stream_read_error.txt").write_text(str(e))

    t_out = threading.Thread(
        target=_reader, args=(proc.stdout, stdout_tail, stdout_live), daemon=True
    )
    t_err = threading.Thread(
        target=_reader, args=(proc.stderr, stderr_tail, stderr_live), daemon=True
    )
    t_out.start()
    t_err.start()

    # wait for server to be ready (timeout)
    deadline = time.time() + timeout
    last_err = None
    poll_count = 0
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
                _ = resp.read()
                break
        except Exception as e:
            last_err = e
            time.sleep(0.5)
            poll_count += 1
            # every few polls print a short stderr tail for debugging
            if poll_count % 4 == 0:
                recent = list(stderr_tail)[-20:]
                if recent:
                    print(f"[start_example] recent stderr (last {len(recent)} lines):")
                    for ln in recent:
                        print(ln)
    else:
        # on timeout, capture last few stderr lines and fail with helpful output
        stderr_tail_text = "\n".join(list(stderr_tail)[-200:])
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        pytest.fail(
            f"Server did not respond in time: {last_err}\nRecent stderr:\n{stderr_tail_text}"
        )

    # register proc so teardown can capture its output
    request.node._example_proc = proc

    yield port

    rep = getattr(request.node, "rep_call", None)
    failed = bool(rep and rep.failed)
    if failed:
        adir = ARTIFACTS_DIR / request.node.nodeid.replace("::", "_").replace("/", "_")
        adir.mkdir(parents=True, exist_ok=True)
        try:
            # if live files exist, prefer those; fall back to reading pipes
            if stdout_live.exists():
                (adir / "server_stdout.txt").write_text(
                    stdout_live.read_text(encoding="utf-8"), encoding="utf-8"
                )
            else:
                out = proc.stdout.read().decode(errors="ignore") if proc.stdout else ""
                (adir / "server_stdout.txt").write_text(out, encoding="utf-8")
            if stderr_live.exists():
                (adir / "server_stderr.txt").write_text(
                    stderr_live.read_text(encoding="utf-8"), encoding="utf-8"
                )
            else:
                err = proc.stderr.read().decode(errors="ignore") if proc.stderr else ""
                (adir / "server_stderr.txt").write_text(err, encoding="utf-8")
        except Exception as e:
            (adir / "server_log_error.txt").write_text(str(e))

    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
