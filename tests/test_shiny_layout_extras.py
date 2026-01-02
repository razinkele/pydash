def test_menu_item_renders_badge_and_link():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import menu_item_shiny

    tag = menu_item_shiny("About", href="#about", badge="3")
    html = str(tag)
    assert "nav-link" in html
    assert "#about" in html
    assert "badge" in html


def test_sidebar_accepts_dict_and_group():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import sidebar_shiny

    menu = [
        ("Home", "#"),
        ("Group", [("A", "#a"), ("B", "#b", "2")]),
        {"text": "About", "href": "#about", "badge": "5"},
    ]

    page = sidebar_shiny(brand_title="X", menu=menu)
    html = str(page)
    assert "brand-text" in html
    assert "Group" in html
    assert "badge" in html


def test_navbar_item_and_breadcrumb():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import (breadcrumb_shiny, navbar_item_shiny,
                            navbar_user_menu_shiny)

    n = navbar_item_shiny("Alerts", href="#alerts", badge="1", icon="fas fa-bell")
    s = str(n)
    assert "Alerts" in s
    assert "badge" in s
    assert "fas fa-bell" in s

    um = navbar_user_menu_shiny(
        "Alice",
        image="/img/alice.png",
        dropdown_items=[("Profile", "#profile"), ("Logout", "#logout")],
    )
    us = str(um)
    assert "dropdown" in us
    assert "Profile" in us
    assert "/img/alice.png" in us

    # fallback initials avatar when no image
    um2 = navbar_user_menu_shiny(
        "Bob Jones", image=None, dropdown_items=[("Profile", "#")]
    )
    s2 = str(um2)
    assert "BJ" in s2
    assert "user-avatar-initials" in s2
    # verify we use classes, not inline styles
    assert "style=" not in s2

    bc = breadcrumb_shiny(("Home", "#"), "Section")
    assert "breadcrumb" in str(bc)
    assert "Section" in str(bc)


def test_sidebar_header_and_divider_and_icons():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import (menu_item_shiny, sidebar_divider_shiny,
                            sidebar_header_shiny)

    hdr = sidebar_header_shiny("Main")
    assert "nav-header" in str(hdr)

    div = sidebar_divider_shiny()
    assert "sidebar-divider" in str(div)

    it = menu_item_shiny("Help", href="#help", icon="fas fa-question-circle")
    assert "fas fa-question-circle" in str(it)
