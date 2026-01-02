from pathlib import Path

from shiny import App, ui

from bs4dash_py import (box_shiny, controlbar_shiny, dashboard_page_shiny,
                        footer_shiny, info_box_shiny, navbar_shiny,
                        sidebar_shiny, value_box_shiny)

# CDNs
ADMINLTE = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css"
ADMINLTE_JS = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

# Read local theme overrides
css_path = Path(__file__).parent / "assets" / "custom_theme.css"
custom_css = css_path.read_text() if css_path.exists() else ""

hdr = navbar_shiny(
    "bs4dash-py Themed MVP",
    controlbar_icon=ui.tags.i({"class": "fas fa-th"}),
    right_ui=[
        {"type": "user", "title": "Themed User", "items": [("Profile", "#profile")]}
    ],
)
side = sidebar_shiny(
    brand_title="MVP Themed",
    menu=[
        ("Home", "#", None, "fas fa-home"),
        ("About", "#about", "1", "fas fa-info-circle"),
        ("Documentation",),
        ("Groups", [("One", "#one", None, "fas fa-circle"), ("Two", "#two", "3")]),
        "DIVIDE",
        {"text": "Help", "href": "#help", "icon": "fas fa-question-circle"},
    ],
)

content = ui.tags.div(
    {"class": "container-fluid pt-3"},
    ui.tags.div(
        {"class": "row"},
        box_shiny(
            ui.tags.p("Hello from themed box"), title="Box 1", status="primary", width=6
        ),
        box_shiny(
            ui.tags.p("Another themed box"), title="Box 2", status="success", width=6
        ),
    ),
    ui.tags.hr(),
    ui.tags.div(
        {"class": "row"},
        ui.tags.div(
            {"class": "col-12"},
            ui.input_action_button("show_cb", "Show controlbar"),
            ui.input_action_button("hide_cb", "Hide controlbar"),
        ),
    ),
    ui.tags.hr(),
    ui.tags.div(
        {"class": "row"},
        value_box_shiny("42", title="Active", color="primary", width=3),
        value_box_shiny("7", title="Alerts", color="danger", width=3),
        info_box_shiny("Users", "123", color="success", width=6),
    ),
)

ftr = footer_shiny(
    text="© 2026 Themed Company",
    left=ui.tags.div(ui.tags.a({"href": "#"}, "Privacy")),
    right=ui.tags.div(ui.tags.a({"href": "#"}, "Contact")),
)

control = controlbar_shiny(
    ui.tags.div({"class": "p-3"}, ui.tags.h5("Controlbar"), ui.tags.p("Some settings"))
)

# Inject custom CSS into the page head so it overrides defaults
style_tag = ui.tags.style(custom_css) if custom_css else None

page = dashboard_page_shiny(
    header=hdr,
    sidebar=side,
    body=content,
    controlbar=control,
    footer=ftr,
    adminlte_css=ADMINLTE,
    adminlte_js=ADMINLTE_JS,
)

# Compose UI with style tag first so overrides apply
app_ui = ui.page_fixed(style_tag, page)


def server(input, output, session):
    from shiny import reactive

    from bs4dash_py import hide_controlbar, show_controlbar

    @reactive.Effect
    def _show_cb_handler():
        if input.show_cb():
            show_controlbar(session)

    @reactive.Effect
    def _hide_cb_handler():
        if input.hide_cb():
            hide_controlbar(session)


app = App(app_ui, server)

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PYBS4DASH_PORT", "8000"))
    app.run(port=port)
