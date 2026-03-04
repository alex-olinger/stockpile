"""Tests for pipeline.workflow.video_gen — scene video orchestration."""

import pytest
from pathlib import Path
from pipeline.workflow.video_gen import generate_scene_videos


def test_generate_scene_videos_dry_run(tmp_path):
    """Dry-run should skip actual video generation and print messages."""
    scene_dir = tmp_path / "test-scene"
    (scene_dir / "base").mkdir(parents=True)

    fake_image = tmp_path / "source.png"
    fake_image.write_bytes(b"fake image")

    image_paths = {"base": fake_image}
    video_prompts = {"base": "Slow camera drift"}

    result = generate_scene_videos(
        image_paths, video_prompts, scene_dir, "test-scene", dry_run=True
    )
    assert "base" in result
    assert result["base"].suffix == ".mp4"


def test_generate_scene_videos_returns_paths(tmp_path):
    """Should return dict mapping keys to video file paths."""
    scene_dir = tmp_path / "test-scene"
    (scene_dir / "base").mkdir(parents=True)

    fake_image = tmp_path / "source.png"
    fake_image.write_bytes(b"fake image")

    image_paths = {"base": fake_image}
    video_prompts = {"base": "Slow camera drift"}

    result = generate_scene_videos(
        image_paths, video_prompts, scene_dir, "test-scene", dry_run=True
    )
    assert isinstance(result, dict)
    assert all(isinstance(v, Path) for v in result.values())
