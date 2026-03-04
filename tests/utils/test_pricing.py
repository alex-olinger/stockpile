"""Tests for pipeline.utils.pricing — pricing table output."""

import pytest
from pipeline.utils.pricing import display_pricing


def test_display_pricing_runs_without_error(capsys):
    """display_pricing() should print output without raising."""
    display_pricing()
    captured = capsys.readouterr()
    assert len(captured.out) > 0


def test_display_pricing_shows_providers(capsys):
    """Output should contain all provider names from the pricing config."""
    display_pricing()
    captured = capsys.readouterr()
    for name in ["Google Gemini", "DALL-E 3", "Flux Pro", "Ideogram",
                  "Kling (fal.ai)", "Runway Gen-3", "Pika", "Luma Dream Machine"]:
        assert name in captured.out
