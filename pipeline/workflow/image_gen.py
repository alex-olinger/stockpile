"""Image generation orchestration — generates a full scene's images from prompts."""

from pathlib import Path

from pipeline.api.image_api import get_image_provider
from pipeline.config import PRICING


def generate_scene_images(
    prompts: dict[str, str],
    scene_image_dir: Path,
    scene_slug: str,
    dry_run: bool = False,
) -> dict[str, Path]:
    """Orchestrate image generation for a complete scene (base + variations).

    Args:
        prompts: Dict with 'base' and 'var1', 'var2', ... keys -> prompt strings.
        scene_image_dir: Path to the scene's image directory.
        scene_slug: Scene slug for file naming.
        dry_run: If True, uses PlaceholderProvider.

    Returns:
        Dict mapping prompt keys to saved image file paths.
    """
    provider = get_image_provider(dry_run=dry_run)
    image_paths = {}

    for key, prompt in prompts.items():
        if key == "base":
            output_path = scene_image_dir / "base" / f"{scene_slug}-base.png"
        else:
            output_path = scene_image_dir / "variations" / f"{scene_slug}-{key}.png"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        provider.generate(prompt, output_path)
        image_paths[key] = output_path
        print(f"  Generated {key}: {output_path.name}")

    cost = PRICING["image"]["gemini"]["cost_per_image"] * len(prompts)
    print(f"\nImage cost: ${cost:.3f} ({len(prompts)} images x ${PRICING['image']['gemini']['cost_per_image']:.3f})")

    return image_paths
