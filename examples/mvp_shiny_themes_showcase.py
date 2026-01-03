from shiny import App, ui

from bs4dash_py import (
    Theme,
    bootswatch_href,
    box_shiny,
    dashboard_page_shiny,
    footer_shiny,
    info_box_shiny,
    navbar_shiny,
)

# CDNs
ADMINLTE = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css"
ADMINLTE_JS = "https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"

# Define three example themes
light_theme = Theme(
    {
        "bs4dash-avatar-bg": "#1f7a8c",
        "bs4dash-badge-info-bg": "#ff6b6b",
        "bs4dash-primary-bg": "#001f3f",
        "bs4dash-tab-fg": "#000000",
        "bs4dash-tab-bg": "#ffffff",
        "bs4dash-nav-active-bg": "#e9ecef",
    }
)

dark_theme = Theme(
    {
        "bs4dash-avatar-bg": "#2b3a42",
        "bs4dash-badge-info-bg": "#6c757d",
        "bs4dash-primary-bg": "#001428",
        "bs4dash-tab-fg": "#ffffff",
        "bs4dash-tab-bg": "#24303a",
        "bs4dash-nav-active-bg": "#20272b",
    }
)

high_contrast_theme = Theme(
    {
        "bs4dash-avatar-bg": "#000000",
        "bs4dash-badge-info-bg": "#ffffff",
        "bs4dash-primary-bg": "#000000",
        "bs4dash-tab-fg": "#000000",
        "bs4dash-tab-bg": "#ffffff",
        "bs4dash-nav-active-bg": "#ffffff",
    }
)

# Initial style tag (light by default)
style_tag = ui.tags.style(light_theme.to_css(), id="theme-styles")

hdr = navbar_shiny("bs4dash Theming Showcase")
side = None

content = ui.tags.div(
    {"class": "container-fluid pt-3"},
    ui.tags.div(
        {"class": "row mb-3"},
        ui.tags.div(
            {"class": "col-12"},
            ui.tags.h3("Choose a theme to apply:"),
            ui.tags.button(
                {"id": "theme-light", "class": "btn btn-outline-primary mr-2"}, "Light"
            ),
            ui.tags.button(
                {"id": "theme-dark", "class": "btn btn-outline-secondary mr-2"}, "Dark"
            ),
            ui.tags.button(
                {"id": "theme-high", "class": "btn btn-outline-dark mr-2"},
                "High contrast",
            ),
            ui.tags.button(
                {"id": "theme-bs-flatly", "class": "btn btn-outline-info mr-2"},
                "Bootswatch: Flatly",
            ),
            ui.tags.button(
                {"id": "theme-bs-cerulean", "class": "btn btn-outline-info mr-2"},
                "Bootswatch: Cerulean",
            ),
            ui.tags.button(
                {"id": "theme-bs-solar", "class": "btn btn-outline-info mr-2"},
                "Bootswatch: Solar",
            ),
            # Small showcase nav with an info badge to observe theme changes
            ui.tags.div(
                {"id": "showcase-nav", "class": "mt-2"},
                ui.tags.ul(
                    {"class": "nav"},
                    ui.tags.li(
                        {"class": "nav-item"},
                        ui.tags.a(
                            {"class": "nav-link active", "href": "#s1"},
                            "Item 1",
                            ui.tags.span({"class": "badge badge-info ml-1"}, "New"),
                        ),
                    ),
                    ui.tags.li(
                        {"class": "nav-item"},
                        ui.tags.a({"class": "nav-link", "href": "#s2"}, "Item 2"),
                    ),
                ),
            ),
        ),
    ),
    ui.tags.div(
        {"class": "row"},
        box_shiny(
            ui.tags.p("Hello from themed box"), title="Box 1", status="primary", width=6
        ),
        box_shiny(
            ui.tags.p("Another themed box"), title="Box 2", status="success", width=6
        ),
    ),
    ui.tags.hr(),
    ui.tags.div(
        {"class": "row"}, info_box_shiny("Users", "123", color="success", width=6)
    ),
)

# small script that holds the CSS and swaps the theme by replacing the style tag content
script = ui.tags.script(
    "(function(){\n"
    "  const themes = {\n"
    f"    light: `{light_theme.to_css()}` ,\n"
    f"    dark: `{dark_theme.to_css()}` ,\n"
    f"    high: `{high_contrast_theme.to_css()}`\n"
    "  };\n"
    "  function apply(name){ try{ document.getElementById('theme-styles').textContent = themes[name]; }catch(e){} try{ var nl = document.querySelectorAll('#showcase-nav .nav-link'); nl.forEach(function(n, i){ n.classList.remove('active'); }); if(nl && nl[0]) nl[0].classList.add('active'); }catch(e){} }\n"
    "  document.getElementById('theme-light').addEventListener('click', function(){ apply('light') });\n"
    "  document.getElementById('theme-dark').addEventListener('click', function(){ apply('dark') });\n"
    "  document.getElementById('theme-high').addEventListener('click', function(){ apply('high') });\n"
    "  document.getElementById('theme-bs-flatly').addEventListener('click', function(){\n"
    f"    try{{ var link = document.getElementById('bootswatch-link'); if(!link){{ link = document.createElement('link'); link.id='bootswatch-link'; link.rel='stylesheet'; document.head.appendChild(link); }} link.href = '{bootswatch_href('flatly')}'; }}catch(e){{}}\n"
    "  });\n"
    "  document.getElementById('theme-bs-cerulean').addEventListener('click', function(){\n"
    f"    try{{ var link = document.getElementById('bootswatch-link'); if(!link){{ link = document.createElement('link'); link.id='bootswatch-link'; link.rel='stylesheet'; document.head.appendChild(link); }} link.href = '{bootswatch_href('cerulean')}'; }}catch(e){{}}\n"
    "  });\n"
    "  document.getElementById('theme-bs-solar').addEventListener('click', function(){\n"
    f"    try{{ var link = document.getElementById('bootswatch-link'); if(!link){{ link = document.createElement('link'); link.id='bootswatch-link'; link.rel='stylesheet'; document.head.appendChild(link); }} link.href = '{bootswatch_href('solar')}'; }}catch(e){{}}\n"
    "  });\n"
    "})();"
)

page = dashboard_page_shiny(
    header=hdr,
    sidebar=side,
    body=content,
    footer=footer_shiny(text="Theming showcase"),
    adminlte_css=ADMINLTE,
    adminlte_js=ADMINLTE_JS,
)

app_ui = ui.page_fixed(style_tag, page, script)


def server(input, output, session):
    pass


app = App(app_ui, server)

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PYBS4DASH_PORT", "8000"))
    app.run(port=port)
