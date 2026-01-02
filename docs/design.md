# bs4dash-py — Discovery & Design

Version: 0.1 (Draft)
Date: 2026-01-02
Authors: Project

---

## 1. Overview (🎯)

**Goal:** implement a Python library that provides AdminLTE3/Bootstrap4-styled dashboard components targeted primarily at Shiny for Python, with a clear API and compatible behaviors with R's bs4Dash where practical.

**MVP scope:** core layout primitives (page, header/navbar, sidebar, body, footer), basic UI components (box/card, value/info boxes, tabs), client-side behaviors (sidebar pushmenu toggle, controlbar), server helpers for updates, examples, tests, and documentation.

**Non-goals (initial):** replicate every bs4Dash feature, provide full React component suite, support both Dash and Shiny in the first release (we support Shiny-first, Dash wrappers optional later).

---

## 2. Design Principles

- Be idiomatic to Shiny for Python (use `shiny.ui`, `render`, and server patterns).
- Keep CSS/JS assets external by default (CDN) but allow bundling into package assets for offline use.
- Prefer small, well-tested JS modules (progressive enhancement) over heavy custom frameworks.
- Avoid copying GPL-licensed R code; reimplement behaviors and reference source as needed.
- Provide minimal components first, then extend with optional advanced components that may require more complex client-side code.

---

## 3. Technology & Version Choices

- Target: Shiny for Python (preferred), Python >= 3.8.
- UI base: AdminLTE v3 (AdminLTE 3.2.x) + Bootstrap 4 (match bs4Dash R choices) for initial parity.
- Theming: simple CSS variable / helper functions; later consider integration with a theming library.
- JS: small assets in `assets/` (no build step for MVP). If advanced components require, move to a small JS build (esbuild/webpack) and React-based components.
- License: start with permissive license (MIT or Apache-2.0). Do a legal check to ensure we don't include GPL code from bs4Dash.

---

## 4. Component Map (R bs4Dash → pybs4dash)

- Layout
  - `dashboardPage` → `dashboard_page_shiny` (wrap page; inject AdminLTE assets and data attributes)
  - `dashboardHeader` → `navbar_shiny`
  - `dashboardSidebar` → `sidebar_shiny` (menu helpers)
  - `dashboardBody` → `body_shiny` / direct use of ui tags
  - `dashboardFooter` → `footer_shiny`

- UI primitives
  - `box` → `box_shiny`
  - `valueBox` / `infoBox` → `value_box_shiny`, `info_box_shiny`
  - `tabBox` / `tabItem` → `tabs_shiny`, `tab_item_shiny`
  - `dropdownMenu` / `userMenu` → `dropdown_menu_shiny`, `user_menu_shiny`

- Utility & helper functions
  - server-side updates: `update_navbar_tabs`, `update_sidebar`, `render_user` → Shiny patterns (Outputs/Inputs)
  - `preloader` support via waiter-like pattern (Shiny for Python compatible)

---

## 5. API & Naming Conventions

- Use `snake_case` for functions.
- Prefer short, explicit function names: e.g., `dashboard_page_shiny`, `navbar_shiny`.
- Provide both simple wrappers (tag helpers) and `*_output`/`render_*` patterns where dynamic content is expected.
- Keep function signatures small; pass additional HTML attributes through `**kwargs` where sensible.

Example usage (MVP):

```py
from shiny import App, ui
from bs4dash_py import dashboard_page_shiny, navbar_shiny, sidebar_shiny, box_shiny

hdr = navbar_shiny("My app")
side = sidebar_shiny(brand_title="MVP", menu=[("Home","#"), ("About","#about")])
content = box_shiny(ui.tags.p("Hello"), title="Box")
page = dashboard_page_shiny(header=hdr, sidebar=side, body=ui.tags.div(content))
app_ui = ui.page_fixed(page)
```

---

## 6. Client-side behaviors

- Implement minimal JS for: pushmenu toggle (collapse/expand), controlbar open/close, tab activation, tooltips (optional), and scroll-to-top.
- Expose clientside events where server integration is needed (e.g., fire custom events that server can listen to or use input bindings if necessary).
- Keep JS unobtrusive and ensure it degrades gracefully without JS.

---

## 7. Server patterns & dynamic updates

- Instead of Shiny's R-specific server helpers, provide Python `update_*` functions that wrap common patterns using Shiny `Output`/`Input` constructs (e.g., replace entire UI sections with `uiOutput`/`render_ui`).
- Provide examples for pattern-matching callbacks where an app wants to update menu items or badges (use unique IDs and `uiOutput`).

---

## 8. Theming & Skinning

- Provide a simple `use_bs4dash_theme()` or helper functions to change colors/status values.
- Allow `adminlte_css` override or `fresh`-style skin integration as future enhancement.
- Consider a `skinSelector` helper component to toggle light/dark and predefined skins.

---

## 9. Testing strategy

- Unit tests for Python helpers (import, basic outputs producing HTML tags with expected classes).
- Integration tests: launch example Shiny apps and assert HTTP endpoints return content (smoke tests). Use local test server in CI.
- Visual/interactive tests (optional): Playwright to ensure components render and JS behaviors work across browsers.

---

## 10. CI & Release plan

- CI: run tests on multiple Python versions; add linting (flake8/ruff), type checks (mypy optional), and pre-commit.
- Release: tag-based releases; publish to PyPI with GitHub Actions after passing CI.
- Documentation site: use docs/ with mkdocs or similar (defer decision until v0.1 API stabilizes).

---

## 11. Accessibility & Security

- Add ARIA roles to key components (sidebar, nav, menus) as part of UI helper templates.
- Avoid rendering unescaped user-provided HTML by default, or document safe ways to pass HTML.
- Run basic axe-core audits for example apps.

---

## 12. License & legal

- Prefer permissive license (MIT or Apache-2.0) to encourage adoption.
- Do not copy code from bs4Dash (GPL); reimplement based on AdminLTE documentation and original AdminLTE sources (MIT/BSD/etc.).
- Document third-party asset licenses (AdminLTE, Bootstrap) in LICENSE and README.

---

## 13. Roadmap & Milestones (short)

1. Discovery & design (this doc) — DONE
2. Project scaffold & infra (CI, hooks) — next
3. Core layout + basic components + unit tests
4. JS bindings for behaviors + integration tests
5. Theming + gallery examples + docs
6. v0.1 release

---

## 14. Risks & mitigations

- Risk: Difference between Shiny and Shiny-for-Python behavior. Mitigation: early prototypes and examples to validate server patterns.
- Risk: Licensing conflicts if copying R code. Mitigation: reimplement and reference original code/concepts only.
- Risk: Heavy JS needed for parity. Mitigation: incremental approach and prefer minimal JS + server-side updates when possible.

---

## 15. Acceptance criteria (for MVP)

- Library provides `dashboard_page_shiny`, `navbar_shiny`, `sidebar_shiny`, `box_shiny`.
- Example Shiny app runs and demonstrates layout and sidebar toggle.
- Unit tests cover import and core helpers; CI builds and runs tests.
- Documentation includes quickstart and component usage.

---

## 16. Next steps

- Implement the project scaffold & CI, then finish core layout components and tests.
- Add more components incrementally and iterate on theming & client-side behaviors.



*End of design doc (draft).*