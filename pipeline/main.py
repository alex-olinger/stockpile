"""Workflow orchestration — sequential pipeline from pricing display through packaging.

Accepts --dry-run flag via argparse. Sequential workflow calling each module.
Uses input() for all user prompts. Handles KeyboardInterrupt for clean exit.
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


def main() -> None:
    """Run the full content pipeline.

    Steps:
        0. Display pricing table
        1. Week selection — prompt for week number, create week dirs
        2. Scene setup — theme, location, image/variation counts, generate slug
        3. Prompt generation — load past prompts, call Claude, save .txt files
        4. Image generation — generate images from prompts
        5. Image review — open explorer, approve/reject, handle regeneration
        6. Metadata generation — Claude vision on approved images
        7. Metadata review — display and allow inline edits
        8. Video prompt generation — Claude vision for video prompts
        9. Video generation — Kling via fal.ai
       10. Video review — approve/reject videos
       11. Package approved content to outputs/
    """
    pass
