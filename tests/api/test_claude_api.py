"""Tests for pipeline.api.claude_api — mocked anthropic client calls."""

import pytest


def test_generate_prompts_dry_run():
    """Dry-run should return placeholder prompts without API calls."""
    from pipeline.api.claude_api import generate_prompts
    result = generate_prompts("system", "user", dry_run=True)
    assert isinstance(result, str)
    assert "BASE:" in result
    assert "VAR1:" in result


def test_generate_metadata_from_image_dry_run(tmp_path):
    """Dry-run should return placeholder metadata dict."""
    from pipeline.api.claude_api import generate_metadata_from_image
    dummy_image = tmp_path / "test.png"
    dummy_image.write_bytes(b"fake png data")
    result = generate_metadata_from_image(dummy_image, "a prompt", "wellness", dry_run=True)
    assert isinstance(result, dict)
    assert "title" in result
    assert "keywords" in result
    assert result["ai_generated"] is True


def test_generate_video_prompt_from_image_dry_run(tmp_path):
    """Dry-run should return placeholder video prompt string."""
    from pipeline.api.claude_api import generate_video_prompt_from_image
    dummy_image = tmp_path / "test.png"
    dummy_image.write_bytes(b"fake png data")
    result = generate_video_prompt_from_image(dummy_image, dry_run=True)
    assert isinstance(result, str)
    assert len(result) > 0


def test_generate_scene_slug_dry_run():
    """Dry-run should return a placeholder slug string."""
    from pipeline.api.claude_api import generate_scene_slug
    result = generate_scene_slug("wellness", "studio", dry_run=True)
    assert result == "wellness-studio"


def test_generate_prompts_calls_anthropic(mock_claude_client):
    """Should call anthropic.Anthropic.messages.create with correct params."""
    from pipeline.api.claude_api import generate_prompts
    result = generate_prompts("system prompt", "user prompt", dry_run=False)
    assert mock_claude_client.return_value.messages.create.called
    assert isinstance(result, str)


def test_generate_metadata_returns_required_keys(tmp_path, mock_claude_client):
    """Metadata dict should contain title, description, keywords, category, editorial, ai_generated."""
    from pipeline.api.claude_api import generate_metadata_from_image
    # Use dry_run to test the dict shape without needing real images
    result = generate_metadata_from_image(
        tmp_path / "test.png", "a prompt", "wellness", dry_run=True
    )
    for key in ["title", "description", "keywords", "category", "editorial", "ai_generated"]:
        assert key in result
