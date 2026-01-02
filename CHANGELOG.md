# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

- Initial project setup and CI configuration.
- Test: increase server startup timeout and capture example stderr on Playwright failures to improve robustness and diagnostics.
- CI: add `docs/ci-flakiness.md` with guidance for Playwright/browser setup, timeouts, and flaky-test triage; include `shiny` in `dev` extras so Playwright tests run in CI.
- Style: pin `isort==7.0.0` and set `profile = "black"` in `pyproject.toml` to reduce formatting flakiness.
