from shiny import ui

# Shiny for Python helpers to build AdminLTE-compatible layouts


def dashboard_page_shiny(
    header=None,
    sidebar=None,
    body=None,
    controlbar=None,
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
        controlbar,
        footer or ui.tags.footer({"class": "main-footer"}),
    ]

    # Prefer an external asset when possible: attempt to use `ui.include_js` to
    # include the packaged asset `bs4dash_py/assets/bs4dash_controlbar.js`.
    # Fall back to inlining the script if the host Shiny doesn't support
    # `ui.include_js` (ensures backward compatibility across py-shiny versions).
    if hasattr(ui, "include_js"):
        controlbar_asset = ui.include_js("bs4dash_py/assets/bs4dash_controlbar.js")
    else:
        # fallback: inline the file content so behavior remains available
        controlbar_asset = ui.tags.script(
            "(function(){\n"
            "    function handle(msg){\n"
            "        var action = msg && msg.action ? msg.action : 'toggle';\n"
            "        var body = document.body;\n"
            "        if(!body) return;\n"
            "        if(action === 'show') body.classList.add('control-sidebar-open');\n"
            "        else if(action === 'hide') body.classList.remove('control-sidebar-open');\n"
            "        else body.classList.toggle('control-sidebar-open');\n"
            "    }\n"
            "    if(window.Shiny && Shiny.addCustomMessageHandler){\n"
            "        Shiny.addCustomMessageHandler('bs4dash_controlbar', handle);\n"
            "    }\n"
            "})();"
        )

    page = ui.tags.div(
        *head_links,
        ui.tags.div(
            {"class": "wrapper"}, *[c for c in wrapper_children if c is not None]
        ),
        ui.tags.script(src=adminlte_js) if adminlte_js else None,
        controlbar_asset,
    )
    return page


def navbar_shiny(
    title="Dashboard", id="dashboard-navbar", right_ui=None, controlbar_icon=None
):
    """Create a navbar; optionally attach right-side UI elements and a controlbar toggle.

    - right_ui: a list of tags to render on the right side
    - controlbar_icon: a tag to use as the controlbar toggle (if provided)
    """
    right_items = right_ui or []
    if controlbar_icon is not None:
        # controlbar toggle placed on the right
        right_items = list(right_items) + [
            ui.tags.li(
                {"class": "nav-item"},
                ui.tags.a(
                    {
                        "id": "controlbar-toggle",
                        "class": "nav-link",
                        "data-widget": "control-sidebar",
                        "href": "#",
                    },
                    controlbar_icon,
                ),
            )
        ]

    return ui.tags.nav(
        {"class": "main-header navbar navbar-expand"},
        ui.tags.ul(
            {"class": "navbar-nav"},
            # sidebar toggle (left)
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
        ui.tags.ul({"class": "navbar-nav ml-auto navbar-right"}, *right_items),
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


def value_box_shiny(value, title=None, icon=None, color=None, width=3, href=None):
    """Create a small value box similar to AdminLTE's `small-box`.

    - value: prominent value (string or tag)
    - title: label below value
    - icon: optional icon tag
    - color: background color class suffix (e.g., 'primary')
    - width: bootstrap column width (1-12)
    - href: optional link for the footer
    """
    cl = "small-box"
    if color:
        cl += f" bg-{color}"

    footer = ui.tags.a({"class": "small-box-footer", "href": href}, "More info") if href else None

    return ui.tags.div(
        {"class": f"col-{width}"},
        ui.tags.div(
            {"class": cl},
            ui.tags.div({"class": "inner"}, ui.tags.h3(value), ui.tags.p(title) if title else None),
            ui.tags.div({"class": "icon"}, icon) if icon else None,
            footer,
        ),
    )


def info_box_shiny(title, value, icon=None, color=None, width=12):
    """Create an AdminLTE-style info box.

    - title: the label/title
    - value: prominent value
    - icon: optional icon tag
    - color: optional status class (e.g., 'danger')
    """
    cl = "info-box"

    icon_tag = ui.tags.span({"class": f"info-box-icon bg-{color}"}, icon) if icon else None
    content = ui.tags.div({"class": "info-box-content"}, ui.tags.span({"class": "info-box-text"}, title), ui.tags.span({"class": "info-box-number"}, value))
    return ui.tags.div({"class": f"col-{width}"}, ui.tags.div({"class": cl}, icon_tag, content))


def tabs_shiny(id, *tabs, nav_class="nav nav-tabs", content_class="tab-content"):
    """Create a simple tabs container.

    - id: container id
    - tabs: tuples of (tab_id, title, content, active=False)
    """
    nav_items = []
    panes = []
    for tab in tabs:
        tab_id, title, content = tab[0], tab[1], tab[2]
        active = tab[3] if len(tab) > 3 else False
        a_cls = "nav-link active" if active else "nav-link"
        pane_cls = "tab-pane active" if active else "tab-pane"
        nav_items.append(ui.tags.li({"class": "nav-item"}, ui.tags.a({"class": a_cls, "data-toggle": "tab", "href": f"#{tab_id}"}, title)))
        panes.append(ui.tags.div({"class": pane_cls, "id": tab_id}, content))

    return ui.tags.div({"id": id}, ui.tags.ul({"class": nav_class}, *nav_items), ui.tags.div({"class": content_class}, *panes))


def tab_item_shiny(tab_id, content, active=False):
    """Create a single tab pane for use with `tabs_shiny` (helper function)."""
    cls = "tab-pane active" if active else "tab-pane"
    return ui.tags.div({"class": cls, "id": tab_id}, content)


def dashboard_brand_shiny(title, color=None, href=None, image=None, opacity=0.8):
    """Create a brand link for the sidebar/header.

    - color: optional background status class (e.g., 'primary')
    - href: optional URL
    - image: optional image URL
    - opacity: image opacity
    """
    cl = "brand-link"
    if color:
        cl = f"brand-link bg-{color}"

    img_tag = None
    if image:
        img_tag = ui.tags.img(
            {
                "src": image,
                "class": "brand-image img-circle elevation-3",
                "style": f"opacity: {opacity}",
            }
        )

    return ui.tags.a(
        {"class": cl, "href": href or "#", "target": "_blank" if href else None},
        img_tag,
        ui.tags.span({"class": "brand-text font-weight-light"}, title),
    )


def controlbar_shiny(*children, dark=True, id="controlbar"):
    """Create a right control sidebar.

    - children: tags to include inside the controlbar
    - dark: whether to use dark style
    """
    cl = (
        "control-sidebar control-sidebar-dark"
        if dark
        else "control-sidebar control-sidebar-light"
    )
    return ui.tags.aside({"class": cl, "id": id}, *children)


def body_shiny(*rows, container_class="container-fluid"):
    """Create a body wrapper (content area) consisting of rows or arbitrary tags.

    Parameters
    - *rows: one or more tags (e.g., `ui.tags.div(class_='row', children=...)`)
    - container_class: outer container class (default: 'container-fluid')
    """
    content = ui.tags.div({"class": "content"}, *rows)
    return ui.tags.div(
        {"class": "content-wrapper"}, ui.tags.div({"class": container_class}, content)
    )


def footer_shiny(text=None, left=None, right=None):
    """Create a footer for the dashboard.

    - text: plain footer text (centered) or None
    - left/right: optional tags or strings to place on left/right sections
    """
    left_tag = (
        left
        if left is not None
        else ui.tags.div({"class": "float-left d-none d-sm-block"})
    )
    right_tag = (
        right
        if right is not None
        else ui.tags.div({"class": "float-right d-none d-sm-block"})
    )
    center = ui.tags.div({"class": "text-center"}, text) if text is not None else None
    return ui.tags.footer({"class": "main-footer"}, left_tag, center, right_tag)
