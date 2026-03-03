"""Tests for pipeline.api.image_api — provider hierarchy, factory function."""

import pytest
from pipeline.api.image_api import (
    ImageProvider,
    GeminiProvider,
    PlaceholderProvider,
    get_image_provider,
)


def test_image_provider_is_abstract():
    """ImageProvider should not be directly instantiable."""
    with pytest.raises(TypeError):
        ImageProvider()


def test_gemini_provider_is_image_provider():
    """GeminiProvider should be a subclass of ImageProvider."""
    assert issubclass(GeminiProvider, ImageProvider)


def test_placeholder_provider_is_image_provider():
    """PlaceholderProvider should be a subclass of ImageProvider."""
    assert issubclass(PlaceholderProvider, ImageProvider)


def test_get_image_provider_dry_run_returns_placeholder():
    """Factory with dry_run=True should always return PlaceholderProvider."""
    provider = get_image_provider(dry_run=True)
    # Stub: will verify isinstance(provider, PlaceholderProvider)
    pytest.skip("Stub — implementation pending")


def test_placeholder_provider_creates_file(tmp_path):
    """PlaceholderProvider.generate should create a PNG file at output_path."""
    pytest.skip("Stub — implementation pending")
