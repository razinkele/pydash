from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

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

    The Theme can optionally reference a Bootswatch theme. Use
    `Theme.from_bootswatch(name)` to create a Theme with a linked
    Bootswatch reference (the actual stylesheet will be returned by
    `Theme.bootswatch_href()` or `Theme.bootswatch_tag()`).
    """

    def __init__(self, variables: Optional[Dict[str, str]] = None):
        self.variables = variables or {}
        self._bootswatch_name: Optional[str] = None
        self._bootswatch_version: Optional[str] = None

    @classmethod
    def from_bootswatch(cls, name: str, version: str = "5") -> "Theme":
        """Create a Theme object that references a Bootswatch theme.

        The returned Theme will have `bootswatch_href()` and `bootswatch_tag()`
        helpers available to obtain the stylesheet reference.
        """
        t = cls({})
        t._bootswatch_name = name
        t._bootswatch_version = version
        return t

    @classmethod
    def from_bslib(cls, data: dict) -> "Theme":
        """Create a Theme from a bslib-like dictionary of arguments.

        This helper maps common bslib theme arguments into the library's
        CSS variable tokens. Supported mappings include: `bg`, `fg`, `primary`,
        `secondary`, `success`, `info`, `warning`, `danger`, and font keys like
        `base_font`, `heading_font`, `code_font`.

        The mapping is intentionally conservative: we only set variables that
        match the library's token naming scheme (e.g., `bs4dash-primary-bg`).
        Additional keys in `data` are ignored.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dict-like object")

        mapping = {
            "bg": ["bs4dash-nav-bg"],
            "fg": ["bs4dash-nav-fg"],
            "primary": ["bs4dash-primary-bg"],
            "secondary": ["bs4dash-secondary-bg"],
            "success": ["bs4dash-success-bg"],
            "info": ["bs4dash-badge-info-bg"],
            "warning": ["bs4dash-warning-bg"],
            "danger": ["bs4dash-danger-bg"],
            "base_font": ["bs4dash-base-font"],
            "heading_font": ["bs4dash-heading-font"],
            "code_font": ["bs4dash-code-font"],
            # Additional convenience mappings
            "border_radius": ["bs4dash-border-radius"],
            "spacing_sm": ["bs4dash-spacing-sm"],
            "spacing_md": ["bs4dash-spacing-md"],
            "spacing_lg": ["bs4dash-spacing-lg"],
        }

        variables = {}
        for k, v in data.items():
            if k in mapping and v is not None:
                for token in mapping[k]:
                    variables[token] = v

        # Special handling for Bootswatch / preset keys
        bootswatch_name = data.get("bootswatch") or data.get("preset")
        theme = cls(variables)
        if bootswatch_name:
            # If preset/preset is a bootswatch name, set bootswatch reference
            try:
                bs_name = str(bootswatch_name)
                # normalize common 'shiny' preset which isn't a bootswatch name
                if bs_name.lower() != "shiny":
                    theme._bootswatch_name = bs_name
            except Exception:
                pass

        return theme

    def bootswatch_href(self) -> Optional[str]:
        """Return the preferred bootswatch href for this Theme (if set).

        Returns a `file://` URI when a vendored copy exists, otherwise a CDN
        URL. Returns None if the Theme was not created via
        `Theme.from_bootswatch()`.
        """
        if not self._bootswatch_name:
            return None
        return bootswatch_href(
            self._bootswatch_name, version=self._bootswatch_version or "5"
        )

    def bootswatch_tag(
        self, as_tag: Optional[bool] = None
    ) -> Optional[Union[str, Any]]:
        """Return a bootswatch link element or href for this Theme.

        Returns None if the Theme was not created via
        `Theme.from_bootswatch()`.
        """
        if not self._bootswatch_name:
            return None
        return bootswatch_tag(
            self._bootswatch_name,
            version=self._bootswatch_version or "5",
            as_tag=as_tag,
        )

    def to_head_elements(
        self, id: Optional[str] = None, link_as_tag: Optional[bool] = None
    ) -> Tuple[Optional[Union[str, Any]], Optional[Union[str, Any]]]:
        """Return (link, style) elements suitable for injection into a page head.

        - link: the Bootswatch stylesheet reference (link tag or href), or None
          if the Theme is not using Bootswatch.
        - style: the Theme CSS/style tag (string or tag-like object) or None if
          the theme has no CSS.

        Parameters
        ----------
        id : Optional[str]
            Optional id to set on the generated `<style>` tag (useful for
            runtime replacement).
        link_as_tag : Optional[bool]
            Controls the shape of the link returned (see `bootswatch_tag`).
        """
        link = self.bootswatch_tag(as_tag=link_as_tag)
        css = self.to_css()
        # Use to_style_tag when there is CSS; otherwise create an empty style
        # tag with the provided id (when Shiny is available) so consumers can
        # rely on a style element existing for runtime replacement.
        if css:
            style = self.to_style_tag(id=id)
        else:
            if ui is None:
                style = ""
            else:
                style = ui.tags.style("", id=id) if id else ui.tags.style("")
        return (link, style)

    def to_css(self) -> str:
        """Render the theme as a CSS string containing custom properties.

        The property names are expected to not include the leading `--`.

        Returns
        -------
        str
            A CSS snippet containing a `:root` rule with custom properties.
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

    def to_style_tag(self, id: Optional[str] = None) -> Union[str, Any]:
        """Return a `shiny.ui.tags.style` element when `shiny` is available.

        If `id` is provided and `shiny.ui` is available the returned tag will
        include the given id attribute. Falls back to returning the raw CSS
        string when `shiny.ui` isn't importable (useful for tests and static
        consumers).

        Parameters
        ----------
        id : Optional[str]
            Optional id attribute to set on the generated `<style>` tag. This
            is useful for runtime replacement of the theme style (e.g., in the
            showcase example that replaces the content of `#theme-styles`).

        Returns
        -------
        Union[str, Any]
            Either a raw CSS string (when Shiny isn't available) or a Shiny
            tag-like object that will be injected into the document head.
        """
        css = self.to_css()
        if not css:
            return ""
        if ui is None:
            return css
        # Only pass id attribute when provided to avoid None attributes
        if id:
            return ui.tags.style(css, id=id)
        return ui.tags.style(css)


def theme_tag(theme: Theme, id: Optional[str] = None) -> Union[str, Any]:
    """Convenience helper to return a style tag for the given Theme.

    Accepts an optional `id` to aid runtime replacement of the injected
    style tag (useful for dynamic theme switching in examples).

    Returns
    -------
    Union[str, Any]
        Either the raw CSS string (if Shiny isn't available) or a Shiny tag
        object.
    """
    return theme.to_style_tag(id=id)


# Asset provider registry and helpers
# Providers are simple callables that accept (name, **kwargs) and return an
# href string (local file:// or CDN) or None to indicate they can't supply
# the asset. Providers are tried in registration order until one returns
# a string.
_asset_providers: dict = {}


def register_asset_provider(kind: str, provider, *, prepend: bool = False):
    """Register an asset provider for a given asset kind.

    provider: Callable[[str, **kwargs], Optional[str]]
    """
    if kind not in _asset_providers:
        _asset_providers[kind] = []
    if prepend:
        _asset_providers[kind].insert(0, provider)
    else:
        _asset_providers[kind].append(provider)


def unregister_asset_provider(kind: str, provider):
    """Unregister a previously registered provider (no-op if not found)."""
    if kind in _asset_providers and provider in _asset_providers[kind]:
        _asset_providers[kind].remove(provider)


def resolve_asset(kind: str, name: str, **kwargs) -> Optional[str]:
    """Try providers for `kind` and return the first non-None href."""
    if not name:
        return None
    providers = _asset_providers.get(kind, [])
    for p in providers:
        try:
            res = p(name, **kwargs)
            if res:
                return res
        except Exception:
            continue
    return None


# Register a default provider for 'bootswatch' that prefers vendored assets
# but returns None if none found so callers can fallback to CDN.


def _default_bootswatch_provider(name: str, version: str = "5") -> Optional[str]:
    if not name:
        return None

    try:
        from pathlib import Path

        local = (
            Path(__file__).parent / "assets" / "bootswatch" / name / "bootstrap.min.css"
        )
        if local.exists():
            return local.resolve().as_uri()
    except Exception:
        pass
    return None


register_asset_provider("bootswatch", _default_bootswatch_provider)


def bootswatch_href(name: str, version: str = "5") -> str:
    """Return the Bootswatch stylesheet href.

    The function consults registered asset providers first. If a provider
    returns a value (e.g., a vendored `file://` URI) it is returned. If no
    provider can resolve the asset, a CDN URL on jsdelivr is returned.
    """
    if not name:
        raise ValueError("theme name is required")

    res = resolve_asset("bootswatch", name, version=version)
    if res:
        return res

    return f"https://cdn.jsdelivr.net/npm/bootswatch@{version}/dist/{name}/bootstrap.min.css"


def bootswatch_tag(
    name: str, version: str = "5", as_tag: Optional[bool] = None
) -> Union[str, Any]:
    """Return a `link` tag referencing the Bootswatch CSS on the CDN.

    Behavior:
    - `as_tag is None` (default): Returns a `ui.tags.link` when `shiny.ui` is
      available, otherwise returns the href string.
    - `as_tag is True`: Always returns a `link` element. If `shiny.ui` is not
      available a plain HTML `<link .../>` string is returned.
    - `as_tag is False`: Always returns the raw href string.

    Returns
    -------
    Union[str, Any]
        A href string or a tag-like object depending on context and `as_tag`.
    """
    href = bootswatch_href(name, version=version)

    # Explicit preference
    if as_tag is True:
        if ui is None:
            return f'<link rel="stylesheet" href="{href}" />'
        return ui.tags.link({"rel": "stylesheet", "href": href})

    if as_tag is False:
        return href

    # Default auto behavior (preserve prior behavior)
    if ui is None:
        return href
    return ui.tags.link({"rel": "stylesheet", "href": href})


def list_vendored_bootswatch() -> list:
    """Return a sorted list of vendored Bootswatch theme names.

    The function inspects the `src/bs4dash_py/assets/bootswatch` directory and
    returns the names of subdirectories that contain a `bootstrap.min.css`
    file. This helper is useful for deterministic CI and tests.
    """
    try:
        from pathlib import Path

        base = Path(__file__).parent / "assets" / "bootswatch"
        if not base.exists():
            return []
        themes = [
            p.name
            for p in base.iterdir()
            if p.is_dir() and (p / "bootstrap.min.css").exists()
        ]
        return sorted(themes)
    except Exception:
        # Best-effort fallback; do not raise from this helper
        return []


def serve_vendored_bootswatch(
    dest_dir: Union[str, Path], themes: Optional[list] = None
) -> list:
    """Copy vendored Bootswatch themes into a provided static directory.

    This is useful when serving static assets from a web app that expects
    files under a particular path (e.g., Flask/ASGI static dir). The function
    copies each vendored theme's `bootstrap.min.css` into
    `dest_dir/<theme>/bootstrap.min.css` and returns a list of target paths.

    Parameters
    ----------
    dest_dir : str | Path
        The destination directory where theme files will be copied.
    themes : Optional[list]
        List of theme names to copy. If omitted, all vendored themes are used.

    Returns
    -------
    list
        List of Paths of files copied.
    """
    import shutil
    from pathlib import Path

    base = Path(__file__).parent / "assets" / "bootswatch"
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    vendored = list_vendored_bootswatch()
    if themes is not None:
        vendored = [t for t in vendored if t in themes]

    copied = []
    for name in vendored:
        src = base / name / "bootstrap.min.css"
        if not src.exists():
            continue
        out_dir = dest / name
        out_dir.mkdir(parents=True, exist_ok=True)
        dst = out_dir / "bootstrap.min.css"
        shutil.copy2(src, dst)
        copied.append(dst)

    return copied
