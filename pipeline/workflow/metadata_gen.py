"""Metadata generation — create metadata JSON and video prompts via Claude vision."""

import json
import shutil
from pathlib import Path

from pipeline.api.claude_api import generate_metadata_from_image, generate_video_prompt_from_image


def create_metadata(
    image_path: Path, prompt: str, theme: str, dry_run: bool = False
) -> dict:
    """Generate metadata for an approved image via Claude vision API.

    Args:
        image_path: Path to the approved image file.
        prompt: The prompt that generated the image.
        theme: Content category (e.g. 'wellness').
        dry_run: If True, returns placeholder metadata dict.

    Returns:
        Metadata dict with keys: title, description, keywords (25-50),
        category, editorial, ai_generated.
    """
    return generate_metadata_from_image(image_path, prompt, theme, dry_run=dry_run)


def create_video_prompts(
    image_paths: dict[str, Path], dry_run: bool = False
) -> dict[str, str]:
    """Generate video motion prompts for each approved image via Claude vision.

    Args:
        image_paths: Dict mapping keys ('base', 'var1', ...) to image file paths.
        dry_run: If True, returns placeholder video prompts.

    Returns:
        Dict mapping the same keys to video prompt strings.
    """
    video_prompts = {}
    for key, image_path in image_paths.items():
        video_prompts[key] = generate_video_prompt_from_image(image_path, dry_run=dry_run)
    return video_prompts


def save_metadata(metadata: dict, path: Path) -> Path:
    """Write metadata dict as formatted JSON to a file.

    Args:
        metadata: The metadata dictionary to save.
        path: Output file path (e.g. scene-slug-metadata.json).

    Returns:
        Path to the saved JSON file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    return path


def copy_metadata_to_video(src_path: Path, video_dir: Path) -> Path:
    """Copy an image metadata JSON file to the corresponding video directory.

    Args:
        src_path: Path to the source metadata JSON in the image directory.
        video_dir: Destination video scene directory.

    Returns:
        Path to the copied metadata file.
    """
    video_dir.mkdir(parents=True, exist_ok=True)
    dest = video_dir / src_path.name
    shutil.copy2(str(src_path), str(dest))
    return dest
