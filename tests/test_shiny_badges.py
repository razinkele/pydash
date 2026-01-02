def test_navbar_item_badge_dict_and_color():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import navbar_item_shiny

    nb = navbar_item_shiny(
        "Alerts",
        href="#alerts",
        badge={"text": "5", "color": "danger"},
        icon="fas fa-bell",
    )
    s = str(nb)
    assert "Alerts" in s
    assert "badge-danger" in s
    assert 'aria-label="Alerts badge 5"' in s


def test_menu_item_badge_dict_and_remove():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import menu_item_shiny

    m = menu_item_shiny(
        "About", href="#about", badge={"text": "3", "class": "badge badge-warning"}
    )
    s = str(m)
    assert "badge-warning" in s
    assert 'aria-label="About badge 3"' in s

    # None or empty badge should not render a badge span
    m2 = menu_item_shiny("About", href="#about", badge=None)
    assert ".badge" not in str(m2)
