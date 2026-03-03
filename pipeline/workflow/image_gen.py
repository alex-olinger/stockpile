"""Image generation orchestration — generates a full scene's images from prompts."""

from pathlib import Path


def generate_scene_images(
    prompts: dict[str, str],
    scene_image_dir: Path,
    scene_slug: str,
    dry_run: bool = False,
) -> dict[str, Path]:
    """Orchestrate image generation for a complete scene (base + variations).

    Reads prompts, calls the configured image provider for each, saves images
    with correct naming ({slug}-base.png, {slug}-var1.png, etc.), and prints
    a cost summary.

    Args:
        prompts: Dict with 'base' and 'var1', 'var2', ... keys → prompt strings.
        scene_image_dir: Path to the scene's image directory.
        scene_slug: Scene slug for file naming.
        dry_run: If True, uses PlaceholderProvider.

    Returns:
        Dict mapping prompt keys to saved image file paths.
    """
    pass
