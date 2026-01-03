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

    # Prefer external assets when possible: include controlbar JS and our
    # stylesheet. Fall back to inlining the content when running from the
    # source tree or when `ui.include_*` helpers aren't available.
    controlbar_asset = None
    style_asset = None

    if hasattr(ui, "include_js"):
        try:
            controlbar_asset = ui.include_js("bs4dash_py/assets/bs4dash_controlbar.js")
        except Exception:
            try:
                from pathlib import Path

                p = Path(__file__).parent / "assets" / "bs4dash_controlbar.js"
                if p.exists():
                    content = p.read_text(encoding="utf-8")
                    controlbar_asset = ui.tags.script(content)
            except Exception:
                controlbar_asset = None

    if hasattr(ui, "include_css"):
        try:
            style_asset = ui.include_css("bs4dash_py/assets/bs4dash_styles.css")
        except Exception:
            try:
                from pathlib import Path

                p = Path(__file__).parent / "assets" / "bs4dash_styles.css"
                if p.exists():
                    style_asset = ui.tags.style(p.read_text(encoding="utf-8"))
            except Exception:
                style_asset = None

    # fallback JS stub if no asset available
    if controlbar_asset is None:
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

    # fallback style stub if no asset available
    if style_asset is None:
        style_asset = ui.tags.style(
            ".user-avatar-initials{display:inline-block;border-radius:50%;font-weight:600;background:#6c757d;color:#fff;text-align:center}.user-avatar-initials.avatar-md{width:32px;height:32px;line-height:32px}"
        )

    # Prefer in-head style inclusion so a11y fixes are applied early
    if style_asset is not None:
        head_links.append(style_asset)

    # Global theme overrides to ensure high-contrast navbar/tabs for a11y
    # Note: intentionally scoped to header/tabs/demo areas to avoid changing
    # the dark sidebar link styles (`.main-sidebar .nav .nav-link`).
    global_override = ui.tags.style(
        """
        /* Global a11y overrides for navbar and tabs */
        nav.navbar .nav-link,
        .nav.nav-tabs .nav-link,
        #demo-navbar .nav .nav-link,
        #example-tabs .nav .nav-link {
            color: #000000 !important;
            background-color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.25rem !important; /* ~20px */
            padding: 0.3rem 0.6rem !important;
            display: inline-block !important;
            border-radius: 6px !important;
        }
        """,
    )
    head_links.append(global_override)

    page = ui.tags.div(
        *head_links,
        ui.tags.div(
            {"class": "wrapper"}, *[c for c in wrapper_children if c is not None]
        ),
        ui.tags.script(src=adminlte_js) if adminlte_js else None,
        controlbar_asset,
    )
    return page


def _normalize_badge(badge):
    """Normalize badge input into (text, class) tuple.

    Accepts either a string (badge text) or a dict with keys 'text' and
    optional 'class' or 'color'. Returns (text, class_attr) or (None, None)
    if badge is falsy.
    """
    if not badge:
        return None, None
    if isinstance(badge, str):
        return badge, "badge badge-info"
    if isinstance(badge, dict):
        text = badge.get("text") or badge.get("badge")
        cls = badge.get("class")
        color = badge.get("color")
        if not cls:
            cls = f"badge badge-{color}" if color else "badge badge-info"
        return text, cls
    # Fallback
    return str(badge), "badge badge-info"


def navbar_item_shiny(title, href="#", badge=None, icon=None):
    """Create a navbar item with optional badge and icon.

    - badge: either a string or a dict {text, class?, color?}. When provided,
      an accessible `aria-label` is added to the badge element.
    """
    children = []
    if icon:
        if isinstance(icon, str):
            children.append(ui.tags.i({"class": icon}))
        else:
            children.append(icon)
    children.append(title)

    # Inline styles to ensure high-contrast navbar anchors (library-level override)
    a_style = "color:#000000;background:#ffffff;padding:0.3rem 0.6rem;font-weight:700;font-size:20px;border-radius:6px;display:inline-block;"

    a = ui.tags.a({"class": "nav-link", "href": href, "style": a_style}, *children)
    btext, bcls = _normalize_badge(badge)
    if btext is not None:
        # add aria-label for accessibility
        a.append(
            ui.tags.span(
                {"class": bcls + " ml-1", "aria-label": f"{title} badge {btext}"}, btext
            )
        )
    return ui.tags.li({"class": "nav-item"}, a)


def _initials_from_name(name: str) -> str:
    """Return initials derived from a display name (e.g., 'Alice Bob' -> 'AB')."""
    try:
        parts = [p for p in str(name).strip().split() if p]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()
    except Exception:
        return ""


def _initials_avatar(name: str, size: int = 32):
    """Create a simple initials avatar tag using CSS classes (no inline styles).

    - size: preferred pixel width (32 default). Maps to `avatar-sm|md|lg` classes.
    """
    initials = _initials_from_name(name)
    # choose size class
    if size <= 24:
        sz = "avatar-sm"
    elif size <= 32:
        sz = "avatar-md"
    else:
        sz = "avatar-lg"
    return ui.tags.span({"class": f"user-avatar-initials {sz} avatar-circle"}, initials)


def navbar_user_menu_shiny(name, image=None, dropdown_items=None, id="user-menu"):
    """Create a user menu in the navbar.

    - name: display name (string or tag)
    - image: optional avatar URL or tag (string class)
    - dropdown_items: iterable of tags or (title, href) tuples
    - id: id attribute for the container
    """
    # Build the toggle link
    toggle_children = []
    if image:
        if isinstance(image, str):
            toggle_children.append(
                ui.tags.img(
                    {
                        "src": image,
                        "class": "img-circle elevation-2",
                        "alt": f"{name}'s avatar",
                    }
                )
            )
        else:
            toggle_children.append(image)
    else:
        # Fallback to initials avatar when no image is provided
        try:
            toggle_children.append(_initials_avatar(name))
        except Exception:
            # degrade gracefully
            toggle_children.append(ui.tags.span({"class": "ml-1"}, name))

    toggle_children.append(ui.tags.span({"class": "ml-1"}, name))

    a = ui.tags.a(
        {
            "class": "nav-link dropdown-toggle navbar-user-toggle",
            "href": "#",
            "data-toggle": "dropdown",
            "aria-expanded": "false",
            "id": id,
            "role": "button",
        },
        *toggle_children,
    )

    # Build dropdown menu
    menu_children = []
    if dropdown_items:
        for it in dropdown_items:
            if isinstance(it, tuple):
                title, href = it
                menu_children.append(
                    ui.tags.a({"class": "dropdown-item", "href": href}, title)
                )
            else:
                menu_children.append(it)
    else:
        menu_children.append(ui.tags.span({"class": "dropdown-item-text"}, "No items"))

    menu = ui.tags.div({"class": "dropdown-menu dropdown-menu-right"}, *menu_children)

    return ui.tags.li({"class": "nav-item dropdown"}, a, menu)


def navbar_shiny(
    title="Dashboard", id="dashboard-navbar", right_ui=None, controlbar_icon=None
):
    """Create a navbar; optionally attach right-side UI elements and a controlbar toggle.

    - right_ui: a list of tags to render on the right side (plain tags or dicts)
    - controlbar_icon: a tag to use as the controlbar toggle (if provided)
    """
    # normalize right_ui entries: allow dicts to specify title/href/badge
    processed = []
    for it in right_ui or []:
        if isinstance(it, dict):
            # Accept user_menu dict shortcut
            if it.get("type") == "user":
                processed.append(
                    navbar_user_menu_shiny(
                        it.get("title", ""),
                        image=it.get("image"),
                        dropdown_items=it.get("items"),
                    )
                )
            else:
                processed.append(
                    navbar_item_shiny(
                        it.get("title", ""),
                        it.get("href", "#"),
                        it.get("badge"),
                        it.get("icon"),
                    )
                )
        else:
            processed.append(it)

    right_items = processed
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
        {"class": "main-header navbar navbar-expand", "aria-label": title},
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


def menu_item_shiny(
    text, href="#", badge=None, active=False, icon=None, is_child=False
):
    """Create a single sidebar menu item.

    - text: link text
    - href: link href
    - badge: optional badge text or dict {text, class?, color?}
    - active: whether to mark item active
    - icon: optional icon (string class or tag)
    - is_child: whether this item is part of a nested submenu (affects ARIA roles)
    """
    a_cls = "nav-link active" if active else "nav-link"

    # build children for anchor: icon (optional) then text
    children = []
    if icon:
        if isinstance(icon, str):
            children.append(ui.tags.i({"class": icon}))
        else:
            children.append(icon)
    children.append(text)

    a = ui.tags.a({"class": a_cls, "href": href}, *children)

    btext, bcls = _normalize_badge(badge)
    if btext is not None:
        # use float-right (sidebar) by default for placement and add aria label
        cls = bcls + " float-right"
        a.append(
            ui.tags.span({"class": cls, "aria-label": f"{text} badge {btext}"}, btext)
        )

    li_attrs = {"class": "nav-item"}
    # For top-level items (not children), expose semantic role 'menuitem' on the LI
    if not is_child:
        li_attrs["role"] = "menuitem"
    else:
        # For nested items, avoid giving them menuitem role; let their container be role=group
        li_attrs["role"] = "none"

    return ui.tags.li(li_attrs, a)


def menu_group_shiny(title, items):
    """Create a simple menu group (collapsible tree) with child items.

    - title: group title
    - items: list of (text, href, badge?, icon?) tuples or dicts
    """
    children = []
    for it in items:
        if isinstance(it, dict):
            text = it.get("text", "")
            href = it.get("href", "#")
            badge = it.get("badge")
            icon = it.get("icon")
        else:
            text, href = it[0], it[1]
            badge = it[2] if len(it) > 2 else None
            icon = it[3] if len(it) > 3 else None
        # nested items are children (is_child=True) so ARIA roles differ
        children.append(menu_item_shiny(text, href, badge, False, icon, is_child=True))

    # Minimal tree markup
    return ui.tags.li(
        {"class": "nav-item has-treeview", "role": "menuitem"},
        ui.tags.a({"class": "nav-link", "tabindex": "0"}, ui.tags.p(title)),
        ui.tags.ul(
            {"class": "nav nav-treeview", "role": "group", "aria-label": title},
            *children,
        ),
    )


def sidebar_shiny(brand_title="My app", menu=None, id="main-sidebar"):
    """Create a sidebar. Menu entries may be:

    - simple tuple: (text, href)
    - tuple with badge: (text, href, badge)
    - dict: {"text":..., "href":..., "badge":...}
    - group: ("Group title", [item, item, ...])
    """
    menu_items = []
    if menu:
        for entry in menu:
            # explicit divider marker
            if isinstance(entry, str) and entry.upper() == "DIVIDE":
                menu_items.append(sidebar_divider_shiny())
                continue

            # header marker (single-element tuple)
            if isinstance(entry, tuple) and len(entry) == 1:
                menu_items.append(sidebar_header_shiny(entry[0]))
                continue

            # group
            if isinstance(entry, tuple) and isinstance(entry[1], list):
                title, items = entry[0], entry[1]
                menu_items.append(menu_group_shiny(title, items))
                continue

            # dict
            if isinstance(entry, dict):
                text = entry.get("text", "")
                href = entry.get("href", "#")
                badge = entry.get("badge")
                active = entry.get("active", False)
                icon = entry.get("icon")
                menu_items.append(menu_item_shiny(text, href, badge, active, icon))
                continue

            # simple tuple or tuple with badge/icon
            try:
                text, href = entry[0], entry[1]
                badge = entry[2] if len(entry) > 2 else None
                icon = entry[3] if len(entry) > 3 else None
                menu_items.append(menu_item_shiny(text, href, badge, False, icon))
            except Exception:
                # ignore malformed entries
                continue

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
            {"class": "card-header"}, ui.tags.h2({"class": "card-title"}, title)
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

    footer = (
        ui.tags.a({"class": "small-box-footer", "href": href}, "More info")
        if href
        else None
    )

    return ui.tags.div(
        {"class": f"col-{width}"},
        ui.tags.div(
            {"class": cl},
            ui.tags.div(
                {"class": "inner"},
                ui.tags.h3(value),
                ui.tags.p(title) if title else None,
            ),
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

    icon_tag = (
        ui.tags.span({"class": f"info-box-icon bg-{color}"}, icon) if icon else None
    )
    content = ui.tags.div(
        {"class": "info-box-content"},
        ui.tags.span({"class": "info-box-text"}, title),
        ui.tags.span({"class": "info-box-number"}, value),
    )
    return ui.tags.div(
        {"class": f"col-{width}"}, ui.tags.div({"class": cl}, icon_tag, content)
    )


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
        nav_items.append(
            ui.tags.li(
                {"class": "nav-item"},
                ui.tags.a(
                    {
                        "class": a_cls,
                        "data-toggle": "tab",
                        "href": f"#{tab_id}",
                        "style": "color:#000000;background:#ffffff;padding:0.3rem 0.6rem;font-weight:700;font-size:20px;border-radius:6px;display:inline-block;",
                    },
                    title,
                ),
            )
        )
        panes.append(ui.tags.div({"class": pane_cls, "id": tab_id}, content))

    return ui.tags.div(
        {"id": id},
        ui.tags.ul({"class": nav_class}, *nav_items),
        ui.tags.div({"class": content_class}, *panes),
    )


def tab_item_shiny(tab_id, content, active=False):
    """Create a single tab pane for use with `tabs_shiny` (helper function)."""
    cls = "tab-pane active" if active else "tab-pane"
    return ui.tags.div({"class": cls, "id": tab_id}, content)


def breadcrumb_shiny(*items):
    """Create breadcrumb markup from strings or (title, href) tuples."""
    parts = []
    for it in items:
        if isinstance(it, tuple):
            title, href = it
            parts.append(
                ui.tags.li(
                    {"class": "breadcrumb-item"}, ui.tags.a({"href": href}, title)
                )
            )
        else:
            parts.append(ui.tags.li({"class": "breadcrumb-item active"}, it))
    return ui.tags.ol({"class": "breadcrumb"}, *parts)


def sidebar_header_shiny(text):
    """Render a sidebar header (visual group header)."""
    # Use role=separator to avoid list semantics issues when used inside the menu
    return ui.tags.li({"class": "nav-header", "role": "separator"}, text)


def sidebar_divider_shiny():
    """Render a horizontal divider for the sidebar."""
    # Return a separator list item so it is a valid child of the menu UL
    return ui.tags.li({"class": "sidebar-divider mt-2 mb-2", "role": "separator"})


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
