from typing import Dict

try:
    # Keep Shiny import lazy for environments without shiny
    from shiny import ui
except Exception:  # pragma: no cover - import-time fallback
    ui = None


class Theme:
    """A minimal Theme helper that emits CSS variables for use in the
    app head. Intended to be small and testable as a first iteration.

    Example:
        t = Theme({"bs4dash-primary": "#0b5e2e", "bs4dash-accent": "#ff6b6b"})
        style = t.to_css()
    """

    def __init__(self, variables: Dict[str, str] | None = None):
        self.variables = variables or {}

    def to_css(self) -> str:
        """Render the theme as a CSS string containing custom properties.

        The property names are expected to not include the leading `--`.
        """
        if not self.variables:
            return ""
        lines = [":root {"]
        for k, v in self.variables.items():
            # normalize name to CSS variable syntax
            name = k if k.startswith("--") else f"--{k}"
            lines.append(f"  {name}: {v};")
        lines.append("}")
        return "\n".join(lines)

    def to_style_tag(self):
        """Return a `shiny.ui.tags.style` element when `shiny` is available.

        Falls back to returning the raw CSS string when `shiny.ui` isn't
        importable (useful for tests and static consumers).
        """
        css = self.to_css()
        if not css:
            return ""
        if ui is None:
            return css
        return ui.tags.style(css)


def theme_tag(theme: Theme):
    """Convenience helper to return a style tag for the given Theme."""
    return theme.to_style_tag()