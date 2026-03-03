"""Tests for pipeline.api.video_api — provider hierarchy, factory function."""

import pytest
from pipeline.api.video_api import (
    VideoProvider,
    KlingProvider,
    PlaceholderVideoProvider,
    get_video_provider,
)


def test_video_provider_is_abstract():
    """VideoProvider should not be directly instantiable."""
    with pytest.raises(TypeError):
        VideoProvider()


def test_kling_provider_is_video_provider():
    """KlingProvider should be a subclass of VideoProvider."""
    assert issubclass(KlingProvider, VideoProvider)


def test_placeholder_video_provider_is_video_provider():
    """PlaceholderVideoProvider should be a subclass of VideoProvider."""
    assert issubclass(PlaceholderVideoProvider, VideoProvider)


def test_get_video_provider_dry_run_returns_placeholder():
    """Factory with dry_run=True should always return PlaceholderVideoProvider."""
    provider = get_video_provider(dry_run=True)
    pytest.skip("Stub — implementation pending")


def test_kling_provider_with_mocked_fal_client():
    """KlingProvider should submit, poll, and download via fal_client."""
    pytest.skip("Stub — implementation pending")
