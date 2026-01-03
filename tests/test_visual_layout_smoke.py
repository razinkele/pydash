def test_visual_layout_structure_and_breadcrumb(start_example, playwright_page):

    # Use fixtures to start example and get a Playwright page helper so artifacts
    # are captured on failure. These fixtures will skip if Playwright isn't
    # available in the environment.
    port = start_example
    page = playwright_page

    page.goto(f"http://127.0.0.1:{port}/", timeout=10000, wait_until="domcontentloaded")

    # Basic structure checks
    assert page.query_selector(".main-header") is not None
    assert page.query_selector(".main-sidebar") is not None
    assert page.query_selector(".content-wrapper") is not None
    assert page.query_selector(".main-footer") is not None

    # Breadcrumb presence
    page.wait_for_selector(".breadcrumb", timeout=5000)
    assert (
        page.evaluate(
            "() => Array.from(document.querySelectorAll('.breadcrumb li')).map(n=>n.textContent).join(' > ')"
        ).strip()
        != ""
    )
