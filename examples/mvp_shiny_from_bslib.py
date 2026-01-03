from shiny import App, ui

from bs4dash_py import (
    Theme,
    bootswatch_href,
    box_shiny,
    dashboard_page_shiny,
    footer_shiny,
    navbar_shiny,
)

ADMINLTE = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css"
ADMINLTE_JS = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

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
    f"    try{{ var link = document.getElementById('bootswatch-link'); if(!link){{ link = document.createElement('link'); link.id='bootswatch-link'; link.rel='stylesheet'; document.head.appendChild(link); }} link.href = '{bootswatch_href('flatly')}'; }}catch(e){{}}\n"
    "  });\n"
    "})();"
)

page = dashboard_page_shiny(
    header=hdr,
    sidebar=side,
    body=content,
    footer=footer_shiny(text="bslib conversion demo"),
    adminlte_css=ADMINLTE,
    adminlte_js=ADMINLTE_JS,
)

app_ui = ui.page_fixed(style_tag, page, script)


def server(input, output, session):
    pass


app = App(app_ui, server)

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PYBS4DASH_PORT", "8000"))
    app.run(port=port)
