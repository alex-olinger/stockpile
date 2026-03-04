"""Pricing display — formatted table of provider costs with availability status."""

import os

from pipeline.config import PRICING


# Map provider keys to the env var that enables them
_PROVIDER_API_KEYS = {
    "gemini": "GOOGLE_API_KEY",
    "dall-e": "GOOGLE_API_KEY",
    "flux": "FAL_KEY",
    "ideogram": "FAL_KEY",
    "kling": "FAL_KEY",
    "runway": "FAL_KEY",
    "pika": "FAL_KEY",
    "luma": "FAL_KEY",
}


def display_pricing() -> None:
    """Print a formatted pricing table for all image and video providers.

    Shows provider name, cost per unit, resolution, and duration (for video).
    Marks providers that have API keys configured in .env vs unconfigured.
    Uses simple terminal formatting (no external table libraries).
    """
    print("\n=== Image Providers ===")
    print(f"{'Provider':<20} {'Cost/Image':>12} {'Resolution':>12} {'Status':>12}")
    print("-" * 58)
    for key, info in PRICING["image"].items():
        env_var = _PROVIDER_API_KEYS.get(key, "")
        status = "Available" if os.getenv(env_var) else "No API key"
        print(f"{info['name']:<20} ${info['cost_per_image']:>10.3f} {info['resolution']:>12} {status:>12}")

    print("\n=== Video Providers ===")
    print(f"{'Provider':<20} {'Cost/Video':>12} {'Duration':>10} {'Resolution':>12} {'Status':>12}")
    print("-" * 68)
    for key, info in PRICING["video"].items():
        env_var = _PROVIDER_API_KEYS.get(key, "")
        status = "Available" if os.getenv(env_var) else "No API key"
        print(f"{info['name']:<20} ${info['cost_per_video']:>10.2f} {info['duration']:>10} {info['resolution']:>12} {status:>12}")
    print()
