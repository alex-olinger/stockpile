"""Shared test fixtures — temp project dirs, mock .env, mock API clients."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a temp directory with the full project directory structure.

    Creates: content/images/, content/videos/, outputs/, rejected/
    Returns the tmp project root path.
    """
    for subdir in [
        "content/images",
        "content/videos",
        "outputs",
        "rejected",
        "archive/by-year",
    ]:
        (tmp_path / subdir).mkdir(parents=True)
    return tmp_path


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch environment variables with test API keys."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")
    monkeypatch.setenv("FAL_KEY", "test-fal-key")


@pytest.fixture
def mock_claude_client(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch anthropic.Anthropic to return canned responses.

    Stubs the Claude API client so tests don't make real API calls.
    """
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='{"title": "Test", "description": "Test desc", "keywords": ["test"], "category": "test", "editorial": false, "ai_generated": true}')]
    mock_client.return_value.messages.create.return_value = mock_response

    monkeypatch.setattr("anthropic.Anthropic", mock_client)
    return mock_client


@pytest.fixture
def mock_image_provider():
    """Return a PlaceholderProvider instance for tests needing images without API calls."""
    from pipeline.api.image_api import PlaceholderProvider
    return PlaceholderProvider()
