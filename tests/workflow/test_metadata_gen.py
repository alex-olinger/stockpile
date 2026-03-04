"""Tests for pipeline.workflow.metadata_gen — metadata dict structure, JSON save/copy."""

import pytest
import json
from pathlib import Path
from pipeline.workflow.metadata_gen import create_metadata, save_metadata, copy_metadata_to_video


def test_create_metadata_dry_run(tmp_path):
    """Dry-run should return placeholder metadata with required keys."""
    dummy_image = tmp_path / "test.png"
    dummy_image.write_bytes(b"fake png data")
    result = create_metadata(dummy_image, "a prompt", "wellness", dry_run=True)
    assert isinstance(result, dict)
    assert "title" in result
    assert result["ai_generated"] is True


def test_save_metadata_writes_json(tmp_path):
    """Should write a valid JSON file at the given path."""
    metadata = {"title": "Test", "keywords": ["a", "b"]}
    path = tmp_path / "test-metadata.json"
    result = save_metadata(metadata, path)
    assert result.exists()
    with open(result) as f:
        loaded = json.load(f)
    assert loaded["title"] == "Test"


def test_copy_metadata_to_video(tmp_path):
    """Should copy metadata JSON from image dir to video dir."""
    src = tmp_path / "image" / "test-metadata.json"
    src.parent.mkdir(parents=True)
    src.write_text('{"title": "Test"}')

    video_dir = tmp_path / "video"
    result = copy_metadata_to_video(src, video_dir)
    assert result.exists()
    assert result.parent == video_dir


def test_metadata_has_required_keys(tmp_path):
    """Metadata dict should contain title, description, keywords, category, editorial, ai_generated."""
    dummy_image = tmp_path / "test.png"
    dummy_image.write_bytes(b"fake png data")
    result = create_metadata(dummy_image, "a prompt", "wellness", dry_run=True)
    for key in ["title", "description", "keywords", "category", "editorial", "ai_generated"]:
        assert key in result
