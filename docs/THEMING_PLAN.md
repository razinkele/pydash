# bs4dash (Python) — Theming & bslib Integration Plan

Date: 2026-01-03

## Summary

This document captures the development plan to finish the bs4dash Python port and integrate theming support (via `bslib` or a lightweight wrapper). It mirrors the TODOs created in the project and provides a short roadmap, acceptance criteria, and next steps.

## Background

- PR merged: #3 — "a11y: fix examples & add test safeguard for demo contrast issues"
- Follow-up issue: #4 — Track demo-only color-contrast items (open)

## Goals

- Provide a clear, testable theming API for bs4dash Python apps.
- Support `bslib`-style theming (CSS variables / Sass fallback) via an appropriate tradeoff: runtime dependency vs wrapper vs vendored assets.
- Ensure themes are testable (Playwright visual + axe accessibility checks) and stable in CI.

## Scope

- API design for themes (Theme object, helpers to apply theme to Shiny apps and static HTML)
- Implementation of a core theming layer (variable injection / stylesheet management)
- Example pages and visual/a11y tests per theme
- CI workflow updates and docs

## Tasks (high level)

- [ ] Audit implementation & tests — file-level review and gap analysis (in-progress)
- [ ] Research `bslib` theming integration — vendor vs wrapper vs runtime dependency
- [ ] Design theming API & extension points (Theme object, use_theme helper, mapping to CSS variables)
- [ ] Implement core bslib support & theme variables (packaging, tests)
- [ ] Update examples & add visual tests (Playwright + axe per theme)
- [ ] Accessibility & contrast sweep (axe runs, computed-contrast checks)
- [ ] CI stabilization & release plan (workflows, caching, release checklist)
- [ ] Docs, migration guide, and tracking issues (how-to, examples)
- [ ] Community review & beta release

## Deliverables

- API spec for theming
- Implementation with tests and examples
- CI workflows that run themed visual tests and collect artifacts
- Documentation and a migration guide

## Acceptance criteria

- Themes can be applied to Shiny apps and static examples with a documented API
- Visual tests and axe audits pass (or documented, tracked exceptions exist)
- PRs and issues created for any follow-up large-scope changes (e.g., AdminLTE core overrides)

## Next steps (immediate)

1. Finish the audit (complete file list, missing features, test coverage gaps).
2. Research `bslib` integration and produce a short recommendation (pros/cons).

---

Notes:
- This plan is intentionally pragmatic: the first objective is to make theming usable and testable; larger, invasive UI/theme changes should be tracked as follow-up issues and handled separately.

(Plan authored by GitHub Copilot, generated on request.)
