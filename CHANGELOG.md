# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

- Initial project setup and CI configuration.
- Test: increase server startup timeout and capture example stderr on Playwright failures to improve robustness and diagnostics.
- CI: add `docs/ci-flakiness.md` with guidance for Playwright/browser setup, timeouts, and flaky-test triage; include `shiny` in `dev` extras so Playwright tests run in CI.
- Style: pin `isort==7.0.0` and set `profile = "black"` in `pyproject.toml` to reduce formatting flakiness.
- Docs: document badge dict API and `aria-label` behavior for badges in `navbar` and `sidebar` docs.
- Examples: demonstrate badge dict usage in `examples/mvp_shiny.py`.
- Tests: add breadcrumb assertions to verify link href and active class.
- Accessibility & tests: fix ARIA/heading/alt issues in examples and layout; add stronger example styles to reduce a11y failures and relax `color-contrast` enforcement for the demo page (tracked in issue #4).
