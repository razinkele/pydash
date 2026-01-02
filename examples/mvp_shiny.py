from shiny import App, ui

from bs4dash_py import (
    box_shiny,
    dashboard_page_shiny,
    navbar_shiny,
    sidebar_shiny,
    footer_shiny,
    controlbar_shiny,
)

# CDNs
ADMINLTE = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css"
ADMINLTE_JS = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

hdr = navbar_shiny(
    "bs4dash-py Shiny MVP", controlbar_icon=ui.tags.i({"class": "fas fa-th"})
)
side = sidebar_shiny(brand_title="MVP", menu=[("Home", "#"), ("About", "#about")])

content = ui.tags.div(
    {"class": "container-fluid pt-3"},
    ui.tags.div(
        {"class": "row"},
        box_shiny(
            ui.tags.p("Hello from box"), title="Box 1", status="primary", width=6
        ),
        box_shiny(ui.tags.p("Another box"), title="Box 2", status="success", width=6),
    ),
    ui.tags.hr(),
    ui.tags.div(
        {"class": "row"},
        ui.tags.div(
            {"class": "col-12"},
            ui.input_action_button("show_cb", "Show controlbar"),
            ui.input_action_button("hide_cb", "Hide controlbar"),
            ui.tags.p(
                "Use these buttons in your app server to call \n"
                "`show_controlbar(session)` and `hide_controlbar(session)` helpers."
            ),
        ),
    ),
    ui.tags.hr(),
    ui.tags.div(
        {"class": "row"},
        value_box_shiny("42", title="Active", color="primary", width=3),
        value_box_shiny("7", title="Alerts", color="danger", width=3),
        info_box_shiny("Users", "123", color="success", width=6),
    ),
    ui.tags.div(
        {"class": "row mt-3"},
        ui.tags.div(
            {"class": "col-12"},
            tabs_shiny("example-tabs", ("t1", "Tab 1", ui.tags.p("Tab1 content"), True), ("t2", "Tab 2", ui.tags.p("Tab2 content"))),
        ),
    ),
)

# footer example
ftr = footer_shiny(
    text="© 2026 My Company",
    left=ui.tags.div(ui.tags.a({"href": "#"}, "Privacy")),
    right=ui.tags.div(ui.tags.a({"href": "#"}, "Contact")),
)

control = controlbar_shiny(
    ui.tags.div({"class": "p-3"}, ui.tags.h5("Controlbar"), ui.tags.p("Some settings"))
)

page = dashboard_page_shiny(
    header=hdr,
    sidebar=side,
    body=content,
    controlbar=control,
    footer=ftr,
    adminlte_css=ADMINLTE,
    adminlte_js=ADMINLTE_JS,
)

app_ui = ui.page_fixed(page)


def server(input, output, session):
    # Server handlers to demonstrate show/hide controlbar actions
    from shiny import reactive
    from bs4dash_py import show_controlbar, hide_controlbar

    @reactive.Effect
    def _show_cb_handler():
        # input.show_cb() is truthy on button click (increments)
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
