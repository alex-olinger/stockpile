"""Main menu + Image/Video mode orchestration.

Two separate modes selectable from a main menu:
- Image Mode (I1-I6): scene setup through image packaging
- Video Mode (V1-V5): scene selection through video packaging

Uses input() for all user prompts. Handles KeyboardInterrupt:
- During a mode → return to main menu
- At main menu → exit program
Passes dry_run boolean to all module functions that make API calls.
"""

import argparse
from pathlib import Path

from pipeline.config import BASE_DIR, IMAGE_DIR, VIDEO_DIR, OUTPUT_DIR, REJECTED_DIR
from pipeline.utils.pricing import display_pricing
from pipeline.utils.file_manager import create_week_dirs, create_scene_dirs, move_to_rejected
from pipeline.workflow.prompt_gen import load_past_prompts, create_prompts, save_prompts
from pipeline.workflow.image_gen import generate_scene_images
from pipeline.workflow.video_gen import generate_scene_videos
from pipeline.workflow.metadata_gen import (
    create_metadata,
    create_video_prompts,
    save_metadata,
    copy_metadata_to_video,
)
from pipeline.workflow.review import review_assets, review_metadata, ask_regenerate
from pipeline.workflow.packaging import package_approved
from pipeline.api.claude_api import generate_scene_slug


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments. Returns namespace with dry_run bool."""
    pass


def select_week() -> Path:
    """Prompt for week number, create/verify week dirs, return week path."""
    pass


def run_image_mode(week_path: Path, dry_run: bool) -> None:
    """Image generation pipeline (Steps I1-I6).

    I1: Scene setup (theme, location, counts, slug, dirs)
    I2: Prompt generation
    I3: Image generation
    I4: Image review
    I5: Metadata generation
    I6: Metadata review + packaging
    """
    pass


def run_video_mode(week_path: Path, dry_run: bool) -> None:
    """Video generation pipeline (Steps V1-V5).

    V1: Scene selection (list existing image scenes)
    V2: Video prompt generation
    V3: Video generation
    V4: Video review
    V5: Packaging
    """
    pass


def main() -> None:
    """Main menu loop.

    Startup: parse args, load env, display pricing.
    Menu: [W]eek select, [I]mage mode, [V]ideo mode, [Q]uit.
    KeyboardInterrupt during mode → return to menu.
    KeyboardInterrupt at menu → exit.
    """
    pass
