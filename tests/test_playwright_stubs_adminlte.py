def test_playwright_adminlte_stub(playwright_page):
    """Verify that AdminLTE CSS/JS requests from CDNs are fulfilled by local stubs."""
    page = playwright_page
    css_url = "https://cdn.jsdelivr.net/npm/admin-lte@3.2.0/dist/css/adminlte.min.css"
    js_url = "https://cdn.jsdelivr.net/npm/admin-lte@3.2.0/dist/js/adminlte.min.js"

    page.goto("data:text/html,<html><head></head><body></body></html>")
    # Add tags referencing CDN URLs; fixture should intercept and inject local assets
    page.add_style_tag(url=css_url)
    page.add_script_tag(url=js_url)

    # Assert stylesheet is present in document.styleSheets
    has_stylesheet = page.evaluate(
        "() => !!Array.from(document.styleSheets).find(s=> s.href && s.href.endsWith('adminlte.min.css'))"
    )
    # Assert script content was injected (script element exists and has text)
    has_script = page.evaluate(
        "() => { const s = Array.from(document.scripts).find(s=> s.src && s.src.endsWith('adminlte.min.js')); return !!(s && s.textContent && s.textContent.length>0); }"
    )
    assert has_stylesheet and has_script
