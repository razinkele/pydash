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

custom_css = ui.tags.style(\"\"\"
:root {
  --bs4dash-avatar-bg: #1f7a8c;
  --bs4dash-avatar-fg: #ffffff;
}
\"\"\")

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
style = theme_tag(my_theme, id="theme-styles")  # optional `id` helps runtime replacement
page = ui.page_fixed(style, page)
```
Converting from bslib-like inputs

If you have a configuration that follows bslib's `bs_theme` arguments, use
`Theme.from_bslib(data)` to convert common arguments into `Theme` variables.
For example:

```py
from bs4dash_py import Theme

bslib_data = {
  "bg": "#111111",
  "fg": "#222222",
  "primary": "#ff00ff",
  "info": "#00ffff",
}

theme = Theme.from_bslib(bslib_data)
# Use as before
style = theme.to_css()
```
Showcase

A small interactive example is provided at `examples/mvp_shiny_themes_showcase.py`.
It demonstrates multiple themes (Light, Dark, High-contrast) and allows you to
switch themes in the browser for quick visual inspection. Use it as a reference
for programmatic theme switching in your app.

Bootswatch themes (CDN-first)

You can also apply Bootswatch themes via CDN to preview and reuse existing
Bootstrap theme palettes. The library provides a small helper `bootswatch_tag(name)`
that returns a `<link>` tag (or an href string when `shiny.ui` is not available)
pointing to the Bootswatch CSS for `name` (see `examples/mvp_shiny_themes_showcase.py`
for an example that injects a `bootswatch-link` into the document head).

Quick examples

```py
from bs4dash_py import bootswatch_tag, bootswatch_href

# Returns a <link> element (when used in a UI context) or a string href
link_tag = bootswatch_tag('flatly')
# Directly get the CDN URL
url = bootswatch_href('flatly')
```

Note: CI/test environments may skip Bootswatch checks when the CDN is unreachable;
alternatively you can vendor a curated subset of Bootswatch themes locally
as a fallback.

Vendoring additional Bootswatch themes

If you prefer deterministic tests and to avoid relying on the CDN, add a
vendored copy of the theme CSS at:

```
src/bs4dash_py/assets/bootswatch/<theme-name>/bootstrap.min.css
```

The library provides a helper `list_vendored_bootswatch()` and `bootswatch_href()`
will prefer a vendored copy (returned as a `file://` URI) when available. After
adding files, update tests or add new ones to reflect newly-vendored themes.


Notes

- We use CSS variables to make theming easy and non-invasive. You can
  override tokens at the `:root` level or within a scope (e.g., inside a
  container) for contextual theming.
- For more advanced theming, add your own stylesheet and override as many
  tokens as needed.
