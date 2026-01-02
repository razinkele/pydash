# CI Flakiness Guidance

CI jobs that run browsers and remote services (Playwright, image capture, network tests) can be flaky due to timing, external downloads, or race conditions. Follow these guidelines to reduce flakiness and make failures actionable:

Quick rules
- Pin tool and hook versions (Black, isort, ruff, pre-commit) in `pyproject.toml` and `.pre-commit-config.yaml` and verify locally with the same versions as the runner.
- Use explicit waits and timeouts in tests that depend on external processes (e.g., increase app startup wait from 20s to 60s) and capture stderr/stdout when failures occur to make debugging easier.
- Skip or mark as non-blocking tests that require large external downloads (Playwright browser binaries) when not available, and fail the job explicitly when the setup step (e.g., `playwright install`) fails.

Playwright & browser-heavy tests
- Install browsers in CI step (`playwright install --with-deps`) and cache the browser downloads when possible to avoid transient network failures.
- Use `pytest.importorskip("playwright.sync_api")` so the test suite gracefully skips browser tests if Playwright is not available.
- Launch browsers in headless mode and wrap browser launch in a try/except that skips tests with a helpful message if launch fails.

Server process tests
- When tests start an example app in a subprocess, pick a free port programmatically and pass it using an env var (e.g., `PYBS4DASH_PORT`).
- Poll the server with a reasonable timeout (60s) and on timeout capture the example process stderr and stdout for diagnostics.
- Ensure example entrypoints fail fast with clear errors when required dependencies are missing (e.g., `ModuleNotFoundError: No module named 'shiny'`).

Flaky test triage
- On intermittent failures, immediately gather:
  - Full job logs (action step logs and the failing test output)
  - Any captured stderr/stdout from example processes
  - The runner environment (OS, Python version, installed package versions)
- Re-run the failing job to determine if the failure is transient. If it repeats, add targeted debugging (longer timeouts, capturing logs, or isolation into a smaller reproducer).

When to make failures blocking
- Keep heavy visual tests non-blocking for normal PRs if they require optional steps (e.g., Playwright browser installs) — make them required only when the project is preparing a release or when visual changes are critical.

Automation & observability
- Upload browser screenshots and captured artifacts to the workflow run when available so reviewers can see contextual UI state.
- Add short, focused diagnostics in tests so a single failing test produces an actionable message (include captured stderr, stack trace, and the failing URL/port).

Examples from this repo
- We increased the app startup timeout in `tests/test_visual_controlbar.py` and capture example stderr on failure.
- We added `shiny` to the `dev` extras so Playwright tests can run in CI.

If you need help triaging a flaky failure, open an issue with the failing run URL and any captured artifacts and I can help investigate.
