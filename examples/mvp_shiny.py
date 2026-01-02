from shiny import App, ui

from bs4dash_py import box_shiny, dashboard_page_shiny, navbar_shiny, sidebar_shiny

# CDNs
ADMINLTE = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css"
ADMINLTE_JS = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

hdr = navbar_shiny("bs4dash-py Shiny MVP")
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
)

page = dashboard_page_shiny(
    header=hdr,
    sidebar=side,
    body=content,
    adminlte_css=ADMINLTE,
    adminlte_js=ADMINLTE_JS,
)

app_ui = ui.page_fixed(page)


def server(input, output, session):
    # placeholder server for MVP
    return


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
