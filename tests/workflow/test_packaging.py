"""Tests for pipeline.workflow.packaging — file copying to outputs/."""

import pytest
from pipeline.workflow.packaging import package_approved


def test_package_approved_creates_output_dir(tmp_project):
    """Should create the output scene directory."""
    week_image = tmp_project / "content" / "images" / "week10_20260302"
    week_video = tmp_project / "content" / "videos" / "week10_20260302"
    week_image.mkdir(parents=True)
    week_video.mkdir(parents=True)

    output_base = tmp_project / "outputs"
    result = package_approved(week_image, week_video, "test-scene", output_base)
    assert result.exists()
    assert result.is_dir()


def test_package_approved_copies_files(tmp_project):
    """Should copy approved images, videos, and metadata to flat output structure."""
    week_image = tmp_project / "content" / "images" / "week10_20260302"
    week_video = tmp_project / "content" / "videos" / "week10_20260302"

    img_exports = week_image / "test-scene" / "exports"
    img_exports.mkdir(parents=True)
    (img_exports / "test-scene-base.png").write_bytes(b"fake image")
    (img_exports / "test-scene-metadata.json").write_text('{"title": "Test"}')

    vid_exports = week_video / "test-scene" / "exports"
    vid_exports.mkdir(parents=True)
    (vid_exports / "test-scene-base.mp4").write_bytes(b"fake video")

    output_base = tmp_project / "outputs"
    result = package_approved(week_image, week_video, "test-scene", output_base)

    assert (result / "test-scene-base.png").exists()
    assert (result / "test-scene-metadata.json").exists()
    assert (result / "test-scene-base.mp4").exists()
