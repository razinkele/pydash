"""Minimal example app demonstrating the MVP helpers."""

import dash
from dash import html

from bs4dash_py import box, dashboard_page, navbar, sidebar

# CDNs
BOOTSTRAP4 = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
ADMINLTE = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css"
JQUERY = "https://code.jquery.com/jquery-3.6.0.min.js"
BOOTSTRAP_BUNDLE = (
    "https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"
)
ADMINLTE_JS = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

external_stylesheets = [BOOTSTRAP4, ADMINLTE]
external_scripts = [JQUERY, BOOTSTRAP_BUNDLE, ADMINLTE_JS]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
)

app.title = "bs4dash-py MVP"

hdr = navbar("bs4dash-py MVP")
side = sidebar(brand_title="MVP", menu=[("Home", "#"), ("About", "#about")])

content = html.Div(
    className="container-fluid pt-3",
    children=[
        html.Div(
            className="row",
            children=[
                box(html.P("Hello from box"), title="Box 1", status="primary", width=6),
                box(html.P("Another box"), title="Box 2", status="success", width=6),
            ],
        )
    ],
)

page = dashboard_page(
    header=hdr,
    sidebar=side,
    body=content,
    adminlte_css=ADMINLTE,
    adminlte_js=ADMINLTE_JS,
)

app.layout = page

if __name__ == "__main__":
    app.run(debug=True)
