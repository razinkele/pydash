# Sidebar helpers 🧭

The sidebar helpers make it easy to build AdminLTE-style side navigation.

Key functions

- `menu_item_shiny(text, href='#', badge=None, active=False, icon=None)`
  - Creates a single sidebar item. `icon` can be an icon class (string) or a tag.
- `menu_group_shiny(title, items)`
  - Creates a collapsible group. `items` are tuples or dicts accepted by `menu_item_shiny`.
- `sidebar_header_shiny(text)`
  - Renders a header label (non-clickable) within the menu.
- `sidebar_divider_shiny()`
  - Renders a horizontal divider (HR) to visually separate sections.
- `sidebar_shiny(brand_title='My app', menu=None, id='main-sidebar')`
  - Top-level sidebar creator. `menu` accepts:
    - tuple: `(text, href)` or `(text, href, badge)` or `(text, href, badge, icon)`
    - dict: `{"text":..., "href":..., "badge":..., "icon":..., "active": True}`
    - group: `("Group title", [items...])`
    - header: `("HeaderTitle",)` (single-element tuple)
    - divider marker: the string `'DIVIDE'` (case-insensitive)

Examples

Create a sidebar with icons, badges, header, group and divider:

```py
from bs4dash_py import sidebar_shiny

menu = [
    ("Home", "#", None, "fas fa-home"),
    ("About", "#about", "1", "fas fa-info-circle"),
    ("Documentation",),  # header
    ("Groups", [("One", "#one", None, "fas fa-circle"), ("Two", "#two", "3")]),
    "DIVIDE",
    {"text": "Help", "href": "#help", "icon": "fas fa-question-circle"},
]

sidebar = sidebar_shiny(brand_title="My App", menu=menu)
```

Server integration

- Use `update_sidebar_badges(session, badges)` to update badges dynamically from the server. The client handler matches links by `href` and updates/creates `.badge` spans in the anchor.
