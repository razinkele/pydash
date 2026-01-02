from shiny import ui

# Shiny for Python helpers to build AdminLTE-compatible layouts


def dashboard_page_shiny(
    header=None,
    sidebar=None,
    body=None,
    footer=None,
    title="bs4dash-py MVP",
    adminlte_css=None,
    adminlte_js=None,
):
    head_links = []
    if adminlte_css:
        head_links.append(ui.tags.link(rel="stylesheet", href=adminlte_css))

    wrapper_children = [
        header
        or ui.tags.nav({"class": "main-header navbar navbar-expand navbar-light"}),
        sidebar
        or ui.tags.aside({"class": "main-sidebar sidebar-dark-primary elevation-4"}),
        ui.tags.div(
            {"class": "content-wrapper"}, body or ui.tags.div({"class": "content"})
        ),
        footer or ui.tags.footer({"class": "main-footer"}),
    ]

    page = ui.tags.div(
        *head_links,
        ui.tags.div({"class": "wrapper"}, *wrapper_children),
        ui.tags.script(src=adminlte_js) if adminlte_js else None,
    )
    return page


def navbar_shiny(title="Dashboard", id="dashboard-navbar"):
    return ui.tags.nav(
        {"class": "main-header navbar navbar-expand"},
        ui.tags.ul(
            {"class": "navbar-nav"},
            ui.tags.li(
                {"class": "nav-item"},
                ui.tags.a(
                    {"class": "nav-link", "id": "pushmenu-toggle", "href": "#"},
                    "\u2261",
                ),
            ),
            ui.tags.li(
                {"class": "nav-item d-none d-sm-inline-block"},
                ui.tags.span({"class": "nav-link"}, title),
            ),
        ),
        id=id,
    )


def sidebar_shiny(brand_title="My app", menu=None, id="main-sidebar"):
    menu_items = []
    if menu:
        for text, href in menu:
            menu_items.append(
                ui.tags.li(
                    {"class": "nav-item"},
                    ui.tags.a({"class": "nav-link", "href": href}, text),
                )
            )
    return ui.tags.aside(
        {"class": "main-sidebar sidebar-dark-primary elevation-4", "id": id},
        ui.tags.a(
            {"class": "brand-link"},
            ui.tags.span({"class": "brand-text font-weight-light"}, brand_title),
        ),
        ui.tags.div(
            {"class": "sidebar"},
            ui.tags.nav(
                {"class": "mt-2"},
                ui.tags.ul(
                    {"class": "nav nav-pills nav-sidebar flex-column", "role": "menu"},
                    *menu_items,
                ),
            ),
        ),
    )


def box_shiny(children, title=None, status=None, width=12):
    cls = "card"
    if status:
        cls += f" card-{status}"
    header = (
        ui.tags.div(
            {"class": "card-header"}, ui.tags.h3({"class": "card-title"}, title)
        )
        if title
        else None
    )
    return ui.tags.div(
        {"class": f"col-{width}"},
        ui.tags.div(
            {"class": cls}, header, ui.tags.div({"class": "card-body"}, children)
        ),
    )
