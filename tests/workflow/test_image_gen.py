"""Tests for pipeline.workflow.image_gen — scene image orchestration."""

import pytest
from pipeline.workflow.image_gen import generate_scene_images


def test_generate_scene_images_dry_run(tmp_path):
    """Dry-run should create placeholder images for base + variations."""
    scene_dir = tmp_path / "test-scene"
    (scene_dir / "base").mkdir(parents=True)
    (scene_dir / "variations").mkdir(parents=True)

    prompts = {"base": "A base prompt", "var1": "A variation"}
    result = generate_scene_images(prompts, scene_dir, "test-scene", dry_run=True)

    assert "base" in result
    assert "var1" in result
    assert result["base"].exists()
    assert result["var1"].exists()


def test_generate_scene_images_returns_paths(tmp_path):
    """Should return dict mapping prompt keys to image file paths."""
    scene_dir = tmp_path / "test-scene"
    (scene_dir / "base").mkdir(parents=True)
    (scene_dir / "variations").mkdir(parents=True)

    prompts = {"base": "A prompt"}
    result = generate_scene_images(prompts, scene_dir, "test-scene", dry_run=True)

    assert isinstance(result, dict)
    assert result["base"].suffix == ".png"
