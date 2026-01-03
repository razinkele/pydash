def test_visual_static_navbar_and_sidebar_badges(start_example, playwright_page):

    import pytest

    # Use fixtures to start example and obtain a Playwright page which will be
    # instrumented to capture artifacts on failure.
    port = start_example
    page = playwright_page

    page.goto(f"http://127.0.0.1:{port}/", timeout=10000)

    # Static sidebar badge (About has badge '1')
    page.wait_for_selector(
        ".main-sidebar .nav a[href='#about'] .badge",
        timeout=5000,
    )
    assert (
        page.evaluate(
            "() => document.querySelector('.main-sidebar .nav a[href=\"#about\"] .badge').textContent"
        )
        == "1"
    )
    # Accessibility: badge should have an aria-label describing it and include the badge text
    aria = page.evaluate(
        "() => document.querySelector('.main-sidebar .nav a[href=\"#about\"] .badge').getAttribute('aria-label')"
    )
    assert aria is not None
    assert "1" in aria
    assert "badge" in aria

    # Static navbar badge (Notifications has badge '2')
    page.wait_for_selector("a.nav-link[href='#notif'] .badge", timeout=5000)
    assert (
        page.evaluate(
            "() => document.querySelector('a.nav-link[href=\"#notif\"] .badge').textContent"
        )
        == "2"
    )
    # Accessibility: navbar badge should have aria-label containing badge text
    aria_nav = page.evaluate(
        "() => document.querySelector('a.nav-link[href=\"#notif\"] .badge').getAttribute('aria-label')"
    )
    assert aria_nav is not None
    assert "2" in aria_nav
    assert "badge" in aria_nav

    # Run an axe-core accessibility audit on the page (inject from CDN).
    # This is a best-effort audit; failures will surface as test failures with details.
    page.add_script_tag(
        url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.3/axe.min.js"
    )
    axe = page.evaluate(
        "async () => { const r = await axe.run(); return {violations: r.violations.map(v=>({id:v.id, impact:v.impact, help:v.help, nodes: v.nodes.map(n=>({html: n.html, target:n.target}))}))}; }"
    )
    violations = axe.get("violations") if isinstance(axe, dict) else []
    if violations:
        # Build a compact message with id and help
        msg_lines = [
            f"{v['id']} ({v.get('impact')}): {v.get('help')}" for v in violations
        ]
        pytest.fail("Accessibility audit failures:\n" + "\n".join(msg_lines))
