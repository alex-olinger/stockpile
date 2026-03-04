"""Package approved content — copy approved images, videos, metadata to outputs/."""

import shutil
from pathlib import Path


def package_approved(
    week_image_dir: Path,
    week_video_dir: Path,
    scene_slug: str,
    output_base: Path,
) -> Path:
    """Copy approved images, videos, and metadata to the outputs directory.

    Creates a flat structure: outputs/weekNN_YYYYMMDD/scene-slug/ containing
    all approved PNGs, MP4s, and metadata JSON files for the scene.

    Args:
        week_image_dir: Path to the scene's image week directory.
        week_video_dir: Path to the scene's video week directory.
        scene_slug: Scene slug for the output subdirectory name.
        output_base: Base outputs/ directory path.

    Returns:
        Path to the created output scene directory.
    """
    week_name = week_image_dir.name
    output_dir = output_base / week_name / scene_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    # Copy from image exports
    image_exports = week_image_dir / scene_slug / "exports"
    if image_exports.exists():
        for f in image_exports.iterdir():
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".json"):
                shutil.copy2(str(f), str(output_dir / f.name))
                copied += 1

    # Copy from video exports
    video_exports = week_video_dir / scene_slug / "exports"
    if video_exports.exists():
        for f in video_exports.iterdir():
            if f.suffix.lower() in (".mp4", ".mov", ".json"):
                shutil.copy2(str(f), str(output_dir / f.name))
                copied += 1

    print(f"\nPackaged {copied} files to {output_dir}")
    return output_dir
