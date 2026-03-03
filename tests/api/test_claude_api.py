"""Tests for pipeline.api.claude_api — mocked anthropic client calls."""

import pytest


def test_generate_prompts_dry_run():
    """Dry-run should return placeholder prompts without API calls."""
    from pipeline.api.claude_api import generate_prompts
    result = generate_prompts("system", "user", dry_run=True)
    # Stub: will be implemented to verify placeholder text is returned
    pytest.skip("Stub — implementation pending")


def test_generate_metadata_from_image_dry_run(tmp_path):
    """Dry-run should return placeholder metadata dict."""
    from pipeline.api.claude_api import generate_metadata_from_image
    pytest.skip("Stub — implementation pending")


def test_generate_video_prompt_from_image_dry_run(tmp_path):
    """Dry-run should return placeholder video prompt string."""
    from pipeline.api.claude_api import generate_video_prompt_from_image
    pytest.skip("Stub — implementation pending")


def test_generate_scene_slug_dry_run():
    """Dry-run should return a placeholder slug string."""
    from pipeline.api.claude_api import generate_scene_slug
    pytest.skip("Stub — implementation pending")


def test_generate_prompts_calls_anthropic(mock_claude_client):
    """Should call anthropic.Anthropic.messages.create with correct params."""
    pytest.skip("Stub — implementation pending")


def test_generate_metadata_returns_required_keys():
    """Metadata dict should contain title, description, keywords, category, editorial, ai_generated."""
    pytest.skip("Stub — implementation pending")
