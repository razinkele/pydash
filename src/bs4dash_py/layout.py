from dash import html

# Simple MVP helpers — return Dash HTML nodes with AdminLTE-compatible classes.


def dashboard_page(
    header=None,
    sidebar=None,
    body=None,
    footer=None,
    title="bs4dash-py MVP",
    adminlte_css=None,
    adminlte_js=None,
):
    """Return a top-level page wrapper. Link to AdminLTE CSS/JS via kwargs or external assets."""
    head_links = []
    if adminlte_css:
        head_links.append(html.Link(rel="stylesheet", href=adminlte_css))

    page = html.Div(
        [
            *head_links,
            html.Div(
                className="wrapper",
                children=[
                    header
                    or html.Nav(
                        className="main-header navbar navbar-expand navbar-light"
                    ),
                    sidebar
                    or html.Aside(
                        className="main-sidebar sidebar-dark-primary elevation-4"
                    ),
                    html.Div(
                        className="content-wrapper",
                        children=body or html.Div(className="content"),
                    ),
                    footer or html.Footer(className="main-footer"),
                ],
            ),
            # Optionally include AdminLTE JS at bottom
            html.Script(src=adminlte_js) if adminlte_js else None,
        ]
    )
    return page


def navbar(title="Dashboard", id="dashboard-navbar"):
    return html.Nav(
        className="main-header navbar navbar-expand",
        children=[
            html.Ul(
                className="navbar-nav",
                children=[
                    html.Li(
                        className="nav-item",
                        children=html.A(
                            "\u2261",
                            href="#",
                            className="nav-link",
                            id="pushmenu-toggle",
                        ),
                    ),
                    html.Li(
                        className="nav-item d-none d-sm-inline-block",
                        children=html.Span(title, className="nav-link"),
                    ),
                ],
            )
        ],
        id=id,
    )


def sidebar(brand_title="My app", menu=None, id="main-sidebar"):
    """Return a very simple sidebar structure — menu is list of (text, href) pairs."""
    menu_items = []
    if menu:
        for text, href in menu:
            menu_items.append(
                html.Li(
                    html.A(text, href=href, className="nav-link"), className="nav-item"
                )
            )
    return html.Aside(
        className="main-sidebar sidebar-dark-primary elevation-4",
        children=[
            html.A(
                className="brand-link",
                children=html.Span(
                    brand_title, className="brand-text font-weight-light"
                ),
            ),
            html.Div(
                className="sidebar",
                children=html.Nav(
                    className="mt-2",
                    children=html.Ul(
                        menu_items,
                        className="nav nav-pills nav-sidebar flex-column",
                        role="menu",
                    ),
                ),
            ),
        ],
        id=id,
    )


def box(children, title=None, status=None, width=12):
    cls = "card"
    if status:
        cls += f" card-{status}"
    return html.Div(
        className=f"col-{width}",
        children=html.Div(
            className=cls,
            children=[
                (
                    html.Div(
                        className="card-header",
                        children=html.H3(title, className="card-title"),
                    )
                    if title
                    else None
                ),
                html.Div(className="card-body", children=children),
            ],
        ),
    )
