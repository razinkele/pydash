import os

from shiny import App, ui

from bs4dash_py import (
    Theme,
    box_shiny,
    dashboard_page_shiny,
    footer_shiny,
    navbar_shiny,
)

# Local helper to control Bootswatch sourcing (cdn vs local vendored)
from ._bootswatch import BOOTSWATCH_DEFAULT_THEME, get_bootswatch_href

# Allow overriding AdminLTE assets via environment variables for CI/local vendoring
ADMINLTE = os.environ.get(
    "PYBS4DASH_ADMINLTE",
    "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css",
)
ADMINLTE_JS = os.environ.get(
    "PYBS4DASH_ADMINLTE_JS",
    "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js",
)

# Two example bslib-like configurations
bslib_light = {
    "bg": "#f8f9fa",
    "fg": "#343a40",
    "primary": "#007bc2",
    "info": "#17a2b8",
    "base_font": "Inter, sans-serif",
}

bslib_dark = {
    "bg": "#1d1f21",
    "fg": "#e2e6ea",
    "primary": "#66b0da",
    "info": "#6c757d",
    "base_font": "Roboto, sans-serif",
}

# Create themes via conversion helper
light_theme = Theme.from_bslib(bslib_light)
dark_theme = Theme.from_bslib(bslib_dark)

# Initial style tag
style_tag = ui.tags.style(light_theme.to_css(), id="theme-styles")

# Bootswatch asset sourcing: allow overriding whether to use a local vendored
# file or the CDN via `PYBS4DASH_BOOTSWATCH_SRC=local|cdn` (default: local). Use
# the small helper in `examples/_bootswatch.py` so tests can import it without
# pulling in the full Shiny stack.

hdr = navbar_shiny("bs4dash bslib conversion demo")
side = None

content = ui.tags.div(
    {"class": "container-fluid pt-3"},
    ui.tags.div(
        {"class": "row mb-3"},
        ui.tags.div(
            {"class": "col-12"},
            ui.tags.h3("Apply themes converted from bslib-like dicts"),
            ui.tags.button(
                {"id": "apply-light", "class": "btn btn-outline-primary mr-2"},
                "Apply Light",
            ),
            ui.tags.button(
                {"id": "apply-dark", "class": "btn btn-outline-secondary mr-2"},
                "Apply Dark",
            ),
            ui.tags.button(
                {"id": "apply-flat-bs", "class": "btn btn-outline-info mr-2"},
                "Bootswatch Flatly",
            ),
        ),
    ),
    ui.tags.div(
        {"class": "row"},
        box_shiny(ui.tags.p("Primary box"), title="Box", status="primary", width=6),
    ),
)

script = ui.tags.script(
    "(function(){\n"
    f"  const themes = {{ light: `{light_theme.to_css()}`, dark: `{dark_theme.to_css()}` }};\n"
    "  function apply(name){ try{ document.getElementById('theme-styles').textContent = themes[name]; }catch(e){} }\n"
    "  document.getElementById('apply-light').addEventListener('click', function(){ apply('light') });\n"
    "  document.getElementById('apply-dark').addEventListener('click', function(){ apply('dark') });\n"
    "  document.getElementById('apply-flat-bs').addEventListener('click', function(){\n"
    f"    try{{ var link = document.getElementById('bootswatch-link'); if(!link){{ link = document.createElement('link'); link.id='bootswatch-link'; link.rel='stylesheet'; document.head.appendChild(link); }} link.href = '{get_bootswatch_href(BOOTSWATCH_DEFAULT_THEME)}'; }}catch(e){{}}\n"
    "  });\n"
    "})();"
)

page = dashboard_page_shiny(
    header=hdr,
    sidebar=side,
    body=content,
    footer=footer_shiny(text="bslib conversion demo"),
    adminlte_css=ADMINLTE if ADMINLTE.startswith("http") else None,
    adminlte_js=ADMINLTE_JS if ADMINLTE_JS.startswith("http") else None,
)

# If local AdminLTE paths are provided, inline them into the page so tests
# in CI do not rely on external CDN resolution.
adminlte_style_tag = None
adminlte_script_tag = None
try:
    if ADMINLTE and os.path.exists(ADMINLTE):
        admin_css = open(ADMINLTE, "r", encoding="utf-8").read()
        adminlte_style_tag = ui.tags.style(admin_css, id="adminlte-styles")
except Exception:
    adminlte_style_tag = None

try:
    if ADMINLTE_JS and os.path.exists(ADMINLTE_JS):
        admin_js = open(ADMINLTE_JS, "r", encoding="utf-8").read()
        adminlte_script_tag = ui.tags.script(admin_js)
except Exception:
    adminlte_script_tag = None

# Compose page; include inlined AdminLTE style/script when available
components = []
if adminlte_style_tag:
    components.append(adminlte_style_tag)
components.append(style_tag)
components.append(page)
if adminlte_script_tag:
    components.append(adminlte_script_tag)
components.append(script)

app_ui = ui.page_fixed(*components)


def server(input, output, session):
    pass


app = App(app_ui, server)

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PYBS4DASH_PORT", "8000"))
    app.run(port=port)
