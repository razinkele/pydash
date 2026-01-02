def test_value_and_info_boxes_html():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import info_box_shiny, value_box_shiny

    v = value_box_shiny("42", title="Count", icon=None, color="primary", width=3)
    assert "small-box" in str(v)
    assert "bg-primary" in str(v)

    i = info_box_shiny("Users", "123", icon=None, color="danger", width=6)
    assert "info-box" in str(i)
    assert "info-box-number" in str(i)


def test_tabs_shiny():
    import pytest

    pytest.importorskip("shiny")
    from bs4dash_py import tabs_shiny

    t = tabs_shiny(
        "tabs1", ("tab1", "One", "Content 1", True), ("tab2", "Two", "Content 2")
    )
    html = str(t)
    assert "nav" in html and "tab-pane" in html
    assert "Content 1" in html and "Content 2" in html
