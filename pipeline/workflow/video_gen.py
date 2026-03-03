"""Video generation orchestration — generates videos from approved images + prompts."""

from pathlib import Path


def generate_scene_videos(
    image_paths: dict[str, Path],
    video_prompts: dict[str, str],
    scene_video_dir: Path,
    scene_slug: str,
    dry_run: bool = False,
) -> dict[str, Path]:
    """Orchestrate video generation for a complete scene.

    For each approved image + video prompt pair, calls the configured video
    provider and saves the result. Prints a cost summary.

    Args:
        image_paths: Dict mapping keys ('base', 'var1', ...) to image file paths.
        video_prompts: Dict mapping the same keys to video motion prompts.
        scene_video_dir: Path to the scene's video directory.
        scene_slug: Scene slug for file naming.
        dry_run: If True, uses PlaceholderVideoProvider.

    Returns:
        Dict mapping keys to saved video file paths.
    """
    pass
