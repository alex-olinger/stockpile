"""Tests for pipeline.utils.file_manager — directory creation, uniqueness, structure."""

import pytest
from pipeline.utils.file_manager import create_week_dirs, create_scene_dirs, move_to_rejected


def test_create_week_dirs_creates_both(tmp_project, monkeypatch):
    """Should create matching week dirs under both images/ and videos/."""
    import pipeline.utils.file_manager as fm
    monkeypatch.setattr(fm, "IMAGE_DIR", tmp_project / "content" / "images")
    monkeypatch.setattr(fm, "VIDEO_DIR", tmp_project / "content" / "videos")

    image_week, video_week = create_week_dirs(10, 2026)
    assert image_week.exists()
    assert video_week.exists()
    assert "week10_" in image_week.name
    assert "week10_" in video_week.name


def test_create_week_dirs_errors_if_exists(tmp_project, monkeypatch):
    """Should raise FileExistsError if week directory already exists."""
    import pipeline.utils.file_manager as fm
    monkeypatch.setattr(fm, "IMAGE_DIR", tmp_project / "content" / "images")
    monkeypatch.setattr(fm, "VIDEO_DIR", tmp_project / "content" / "videos")

    create_week_dirs(10, 2026)
    with pytest.raises(FileExistsError):
        create_week_dirs(10, 2026)


def test_create_scene_dirs_creates_subdirs(tmp_path):
    """Should create base/, variations/, exports/ under the scene directory."""
    week_path = tmp_path / "week10_20260302"
    week_path.mkdir()

    scene_dir = create_scene_dirs(week_path, "sunny-beach-scene")
    assert (scene_dir / "base").is_dir()
    assert (scene_dir / "variations").is_dir()
    assert (scene_dir / "exports").is_dir()


def test_move_to_rejected(tmp_project):
    """Should move file to rejected/weekNN/scene-slug/ directory."""
    # Create a dummy file to reject
    src = tmp_project / "test-image.png"
    src.write_text("fake image data")

    rejected_base = tmp_project / "rejected"
    dest = move_to_rejected(src, rejected_base, "week10_20260302", "sunny-beach")

    assert dest.exists()
    assert not src.exists()
    assert "rejected" in str(dest)
    assert "sunny-beach" in str(dest)
