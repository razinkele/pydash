# Breadcrumb helpers 🧭

- `breadcrumb_shiny(*items)`
  - Create breadcrumb markup. Each `item` is either a string (active item) or a `(title, href)` tuple for links.

Example

```py
from bs4dash_py import breadcrumb_shiny

bc = breadcrumb_shiny(("Home", "/"), ("Docs", "/docs"), "Current page")
```

This renders a breadcrumb ordered list with appropriate `breadcrumb-item` classes.
