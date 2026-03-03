"""Tests for pipeline.config — config loading, path constants, pricing structure."""

import pytest
from pipeline.config import BASE_DIR, IMAGE_DIR, VIDEO_DIR, OUTPUT_DIR, REJECTED_DIR, PRICING


def test_base_dir_exists():
    """BASE_DIR should point to the project root containing CLAUDE.md."""
    assert BASE_DIR.exists()


def test_path_constants_are_under_base_dir():
    """All directory constants should be subdirectories of BASE_DIR."""
    for path in [IMAGE_DIR, VIDEO_DIR, OUTPUT_DIR, REJECTED_DIR]:
        assert str(path).startswith(str(BASE_DIR))


def test_pricing_dict_has_image_and_video():
    """PRICING should have 'image' and 'video' top-level keys."""
    assert "image" in PRICING
    assert "video" in PRICING


def test_pricing_image_providers_have_required_keys():
    """Each image provider entry should have name, cost_per_image, resolution."""
    for provider in PRICING["image"].values():
        assert "name" in provider
        assert "cost_per_image" in provider
        assert "resolution" in provider


def test_pricing_video_providers_have_required_keys():
    """Each video provider entry should have name, cost_per_video, duration, resolution."""
    for provider in PRICING["video"].values():
        assert "name" in provider
        assert "cost_per_video" in provider
        assert "duration" in provider
        assert "resolution" in provider
