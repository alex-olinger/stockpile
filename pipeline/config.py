"""Configuration — API keys from .env, pricing data, path constants.

Loads .env via python-dotenv. Exposes API key constants, pricing dict,
and directory path constants for the project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# --- Path constants ---

BASE_DIR: Path = Path(__file__).resolve().parent.parent
"""Project root directory."""

IMAGE_DIR: Path = BASE_DIR / "content" / "images"
"""Base directory for image content, containing weekNN_YYYYMMDD/ folders."""

VIDEO_DIR: Path = BASE_DIR / "content" / "videos"
"""Base directory for video content, mirroring image week structure."""

OUTPUT_DIR: Path = BASE_DIR / "outputs"
"""Packaged approved content for manual upload."""

REJECTED_DIR: Path = BASE_DIR / "rejected"
"""Rejected assets, organized by week/scene."""


def load_env() -> None:
    """Load environment variables from .env file using python-dotenv."""
    global ANTHROPIC_API_KEY, GOOGLE_API_KEY, FAL_KEY
    load_dotenv()
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FAL_KEY = os.getenv("FAL_KEY")


def get_api_key(name: str) -> str | None:
    """Return the value of an API key env var, or None if not set.

    Args:
        name: Environment variable name (e.g. 'ANTHROPIC_API_KEY').
    """
    return os.getenv(name)


# --- API key constants (populated after load_env) ---

ANTHROPIC_API_KEY: str | None = None
GOOGLE_API_KEY: str | None = None
FAL_KEY: str | None = None

# --- Pricing data (manually maintained) ---

PRICING: dict = {
    "image": {
        "gemini": {"name": "Google Gemini", "cost_per_image": 0.039, "resolution": "1920x1080"},
        "dall-e": {"name": "DALL-E 3", "cost_per_image": 0.080, "resolution": "1792x1024"},
        "flux": {"name": "Flux Pro", "cost_per_image": 0.055, "resolution": "1920x1080"},
        "ideogram": {"name": "Ideogram", "cost_per_image": 0.080, "resolution": "1920x1080"},
    },
    "video": {
        "kling": {"name": "Kling (fal.ai)", "cost_per_video": 0.90, "duration": "10s", "resolution": "1920x1080"},
        "runway": {"name": "Runway Gen-3", "cost_per_video": 2.00, "duration": "10s", "resolution": "1920x1080"},
        "pika": {"name": "Pika", "cost_per_video": 0.60, "duration": "4s", "resolution": "1920x1080"},
        "luma": {"name": "Luma Dream Machine", "cost_per_video": 0.50, "duration": "5s", "resolution": "1920x1080"},
    },
}

# --- Claude model config ---

CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
"""Default Claude model for all API calls."""
