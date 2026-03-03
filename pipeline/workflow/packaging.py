"""Package approved content — copy approved images, videos, metadata to outputs/."""

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
    Prints a summary of packaged content.

    Args:
        week_image_dir: Path to the scene's image week directory.
        week_video_dir: Path to the scene's video week directory.
        scene_slug: Scene slug for the output subdirectory name.
        output_base: Base outputs/ directory path.

    Returns:
        Path to the created output scene directory.
    """
    pass
