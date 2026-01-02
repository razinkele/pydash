def test_visual_footer():
    import os
    import sys
    import subprocess
    import socket
    import time
    import urllib.request
    import pytest

    pytest.importorskip("shiny")

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
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
                    html = resp.read().decode("utf-8")
                    assert "main-footer" in html
                    return
            except Exception as e:
                last_err = e
                time.sleep(0.5)
        pytest.fail(f"Server did not respond in time: {last_err}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
