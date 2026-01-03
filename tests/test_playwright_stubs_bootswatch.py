def test_playwright_bootswatch_stub(playwright_page):
    """Verify Bootswatch theme CSS from CDN is satisfied by local stub."""
    page = playwright_page
    css_url = (
        "https://cdn.jsdelivr.net/npm/bootswatch@5.2.3/dist/cyborg/bootstrap.min.css"
    )

    page.goto("data:text/html,<html><head></head><body></body></html>")
    page.add_style_tag(url=css_url)

    has_stylesheet = page.evaluate(
        "() => !!Array.from(document.styleSheets).find(s=> s.href && s.href.endsWith('bootstrap.min.css'))"
    )
    assert has_stylesheet
