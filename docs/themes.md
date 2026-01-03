# Theming & CSS variables 🎨

bs4dash-py exposes a small set of CSS variables (tokens) you can override
in your app to customize colors and sizes without touching library code.

Available variables (defaults are set in `bs4dash_styles.css`):

- `--bs4dash-avatar-bg` — background color for initials avatar (default `#6c757d`)
- `--bs4dash-avatar-fg` — foreground color for initials avatar text (default `#ffffff`)
- `--bs4dash-avatar-sm-size` / `--bs4dash-avatar-md-size` / `--bs4dash-avatar-lg-size` — avatar sizes
- `--bs4dash-avatar-sm-font` / `--bs4dash-avatar-md-font` / `--bs4dash-avatar-lg-font` — avatar font sizes

How to override

Add a small CSS snippet to your Shiny UI (example using `ui.tags.style`):

```py
from shiny import ui

custom_css = ui.tags.style("""
:root {
  --bs4dash-avatar-bg: #1f7a8c;
  --bs4dash-avatar-fg: #ffffff;
}
""")

page = ui.page_fixed(custom_css, ...)
```

Or place an overriding CSS file in your app's static assets and ensure it
is included after the library CSS so your values take precedence.

## Using the `Theme` helper (programmatic theming)

A minimal `Theme` helper is provided (`bs4dash_py.Theme`) that emits CSS custom
properties and a convenience helper `theme_tag` to inject them into the page
head. This is useful for generating themes programmatically from configuration
or for examples.

Example:

```py
from bs4dash_py import Theme, theme_tag

my_theme = Theme({
  "bs4dash-avatar-bg": "#1f7a8c",
  "bs4dash-badge-info-bg": "#ff6b6b",
  "bs4dash-primary-bg": "#001f3f",
})

# Inject into your UI head
style = theme_tag(my_theme)
page = ui.page_fixed(style, page)
```

Notes

- We use CSS variables to make theming easy and non-invasive. You can
  override tokens at the `:root` level or within a scope (e.g., inside a
  container) for contextual theming.
- For more advanced theming, add your own stylesheet and override as many
  tokens as needed.