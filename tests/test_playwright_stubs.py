def test_playwright_cdn_stub(playwright_page):
    """Verify that CDN requests for axe-core are stubbed and expose a working `axe.run()` API."""
    page = playwright_page
    axe_url = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.3/axe.min.js"
    # load a minimal page and inject the axe script via CDN URL; our fixture should
    # intercept and fulfill with the local stub so the script is available synchronously.
    page.goto("data:text/html,<html><head></head><body></body></html>")
    page.add_script_tag(url=axe_url)
    res = page.evaluate(
        "async () => { if(typeof axe === 'undefined') return 'noaxe'; const r = await axe.run(); return Array.isArray(r.violations) ? r.violations.length : 'bad'; }"
    )
    assert res == 0
