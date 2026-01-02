# Navbar helpers 🧾

Convenience helpers for building the top navbar.

Key functions

- `navbar_item_shiny(title, href='#', badge=None, icon=None)`
  - Create a right-side navbar item with optional badge and icon.
- `navbar_shiny(title='Dashboard', id='dashboard-navbar', right_ui=None, controlbar_icon=None)`
  - Create the top navbar. `right_ui` accepts a list of tags or dicts like `{"title": "X", "href": "#", "badge": "1", "icon": "fas fa-bell"}`; dicts will be converted to `navbar_item_shiny` automatically.

Examples

Add an alerts button with a badge on the right:

```py
from bs4dash_py import navbar_shiny
from shiny import ui

alerts = {"title": "Alerts", "href": "#alerts", "badge": "2", "icon": "fas fa-bell"}
nav = navbar_shiny("My App", right_ui=[alerts], controlbar_icon=ui.tags.i({"class": "fas fa-cog"}))
```

Notes

- Badges are rendered with `badge badge-info` classes by default.
- The `controlbar_icon` is placed on the far right and uses the same client-side controlbar handler if present.

User menu

- `navbar_user_menu_shiny(name, image=None, dropdown_items=None)` renders a standard AdminLTE-style user dropdown in the navbar.
- When `image` is not provided, the helper will create a simple initials avatar (derived from the display name) as a fallback.
- For convenience you can pass a dict to `navbar_shiny(right_ui=[...])` with `{"type": "user", "title": "Alice", "image": "/img/alice.png", "items": [("Profile","#"), ("Logout","#logout")]}` and it will be converted to a user menu automatically.
