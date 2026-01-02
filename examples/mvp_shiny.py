from shiny import App, ui

from bs4dash_py import (box_shiny, controlbar_shiny, dashboard_page_shiny,
                        footer_shiny, info_box_shiny, navbar_shiny,
                        sidebar_shiny, tabs_shiny, value_box_shiny)

# CDNs
ADMINLTE = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css"
ADMINLTE_JS = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

hdr = navbar_shiny(
    "bs4dash-py Shiny MVP",
    controlbar_icon=ui.tags.i({"class": "fas fa-th"}),
    right_ui=[
        {
            "type": "user",
            "title": "Alice",
            "image": "https://via.placeholder.com/32",
            "items": [("Profile", "#profile"), ("Logout", "#logout")],
        },
        {
            "type": "user",
            "title": "Bob Jones",
            "items": [("Profile", "#profile"), ("Logout", "#logout")],
        },
    ],
)
side = sidebar_shiny(
    brand_title="MVP",
    menu=[
        ("Home", "#", None, "fas fa-home"),
        ("About", "#about", "1", "fas fa-info-circle"),
        ("Main",),
        {"text": "Sections", "href": "#", "icon": "fas fa-th"},
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
            tabs_shiny(
                "example-tabs",
                ("t1", "Tab 1", ui.tags.p("Tab1 content"), True),
                ("t2", "Tab 2", ui.tags.p("Tab2 content")),
            ),
        ),
    ),
    ui.tags.hr(),
    ui.tags.div(
        {"class": "row"},
        ui.tags.div(
            {"class": "col-12"},
            ui.tags.h5("Dynamic update demos"),
            ui.input_action_button("bs_update_sidebar_badges", "Update sidebar badges"),
            ui.input_action_button("bs_update_navbar_items", "Update navbar items"),
            ui.input_action_button("bs_update_tab_content", "Update tab content"),
            # Demo navbar to be updated
            ui.tags.div(
                {"id": "demo-navbar", "class": "mt-3"},
                ui.tags.ul(
                    {"class": "nav"},
                    ui.tags.li(
                        {"class": "nav-item"},
                        ui.tags.a({"class": "nav-link", "href": "#a"}, "Initial"),
                    ),
                ),
            ),
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

    from bs4dash_py import hide_controlbar, show_controlbar

    @reactive.Effect
    def _show_cb_handler():
        # input.show_cb() is truthy on button click (increments)
        if input.show_cb():
            show_controlbar(session)

    @reactive.Effect
    def _hide_cb_handler():
        if input.hide_cb():
            hide_controlbar(session)

    # Dynamic update handlers
    from bs4dash_py import (update_navbar_items, update_sidebar_badges,
                            update_tab_content)

    @reactive.Effect
    def _update_sidebar_badges():
        if input.bs_update_sidebar_badges():
            # set a badge on the About link (href '#about')
            update_sidebar_badges(session, [{"href": "#about", "badge": "9"}])

    @reactive.Effect
    def _update_navbar_items():
        if input.bs_update_navbar_items():
            items = [
                {"title": "One", "href": "#one", "badge": "1"},
                {"title": "Two", "href": "#two"},
            ]
            update_navbar_items(session, "demo-navbar", items)

    @reactive.Effect
    def _update_tab_content():
        if input.bs_update_tab_content():
            update_tab_content(
                session, "t1", "<p><strong>Updated from server</strong></p>"
            )


app = App(app_ui, server)

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PYBS4DASH_PORT", "8000"))
    app.run(port=port)
