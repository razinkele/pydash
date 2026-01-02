def test_dashboard_brand_shiny_with_image_and_href():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import dashboard_brand_shiny

    tag = dashboard_brand_shiny(
        "MyBrand", image="/img/logo.png", href="https://example.com", opacity=0.9
    )
    s = str(tag)
    assert "brand-link" in s
    assert "brand-image" in s
    assert 'target="_blank"' in s


def test_navbar_shiny_right_ui_and_controlbar_icon():
    import pytest

    pytest.importorskip("shiny")
    from shiny import ui

    from bs4dash_py import navbar_shiny

    right_ui = [
        {
            "type": "user",
            "title": "Alice",
            "image": "/img/alice.png",
            "items": [("P", "#p")],
        },
        {"title": "Alerts", "href": "#alerts", "badge": "2", "icon": "fas fa-bell"},
    ]

    icon = ui.tags.i({"class": "fas fa-th"})

    nav = navbar_shiny("Title", right_ui=right_ui, controlbar_icon=icon)
    s = str(nav)
    # user menu and alert should be present
    assert "dropdown" in s
    assert "Alerts" in s
    # controlbar toggle id should appear
    assert 'id="controlbar-toggle"' in s


def test_menu_group_shiny_and_subitems():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import menu_group_shiny

    group = menu_group_shiny("Group", [("A", "#a"), ("B", "#b", "7")])
    s = str(group)
    assert "has-treeview" in s
    assert "nav-treeview" in s
    assert "#b" in s
    assert "badge" in s


def test_controlbar_shiny_dark_and_light():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import controlbar_shiny

    dark = controlbar_shiny("x", dark=True)
    assert "control-sidebar-dark" in str(dark)

    light = controlbar_shiny("x", dark=False)
    assert "control-sidebar-light" in str(light)


def test_tab_item_shiny_id_and_active():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import tab_item_shiny

    t = tab_item_shiny("t1", "<p>Hi</p>", active=True)
    s = str(t)
    assert 'id="t1"' in s
    assert "tab-pane active" in s
