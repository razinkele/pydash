def test_create_thumbnail(tmp_path):
    import pytest

    try:
        from PIL import Image
    except Exception:
        pytest.skip("Pillow not available")
    from scripts.capture_gallery_screenshots import create_thumbnail

    # Create a dummy image
    img = Image.new("RGB", (1200, 800), "white")
    img_path = tmp_path / "example.png"
    img.save(img_path)

    thumb_dir = tmp_path / "thumbs"
    out = create_thumbnail(img_path, thumb_dir, max_width=400)

    assert out.exists()
    with Image.open(out) as t:
        w, h = t.size
        assert w <= 400
        assert h > 0
