"""Pricing display — formatted table of provider costs with availability status."""

from pipeline.config import PRICING


def display_pricing() -> None:
    """Print a formatted pricing table for all image and video providers.

    Shows provider name, cost per unit, resolution, and duration (for video).
    Marks providers that have API keys configured in .env vs unconfigured.
    Uses simple terminal formatting (no external table libraries).
    """
    pass
